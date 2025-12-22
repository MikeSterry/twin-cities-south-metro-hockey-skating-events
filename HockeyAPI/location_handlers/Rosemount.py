from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from utils.Web_Utils import fetch_content
from datetime import datetime, timedelta
import pdfplumber
import io

class Rosemount:
    """
    Handler for Rosemount Ice Arena open skate events.
    """
    def __init__(self) -> None:
        self.root_url = "https://www.rosemountmn.gov/DocumentCenter/View/4845/2025-December-Arena-Events"

        self.standard_cost = Cost(2.00)
        self.vacation_cost = Cost(6.00)

        address = Address(
            street = "13885 South Robert Trail",
            city = "Rosemount",
            state = "MN",
            zip_code = "55068"
        )
        self.rosemount_ice_arena = Arena(
            name="Rosemount Ice Arena",
            address=address
        )

    """
    Fetch and parse open skate events from the Rosemount Ice Arena PDF calendar.
    Returns:
        list[Event]: A list of Event objects representing open skate sessions.
    """
    def get_events(self) -> list[Event]:
        events = []

        try:
            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.strftime("%B")

            # You can tell the day by the first line in the cell.
            # e.x. "Cell: 14"
            # Cells will contain the words "Open Skate" for open skate times and the following lines will contain the time range.
            # e.x. "Sunday Open Skate:
            # 1:30-3:00pm
            # Note: There are different types of open skate like Daytime Open Skate, Sunday Open Skate, Vacation Open Skate, etc.
            # Also note: when the cell crosses into the next month, the day number will contain a slash (e.x. "Cell: 1/1" for Jan 1st) and you'll need to account for year flips

            pdf_data_bytes = fetch_content(self.root_url)
            pdf_stream = io.BytesIO(pdf_data_bytes)
            with pdfplumber.open(pdf_stream) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if self.validate_calendar_page(page_text, current_month, current_year):
                        tables = page.extract_table()
                        events = self.extract_events_from_pdf_table(tables=tables)
        except Exception as e:
            print(f"An error occurred while fetching Rosemount events: {e}")

        return events

    """
    Validate if the PDF page corresponds to the target month and year.
    Args:
        page_text (str): The text content of the PDF page.
        month (str): The target month (e.g., "December").
        year (int): The target year (e.g., 2025).
    Returns:
        bool: True if the page contains the target month and year, False otherwise.
    """
    @staticmethod
    def validate_calendar_page(page_text, month, year) -> bool:
        target_string = f"{month} {year}"
        return target_string in page_text

    """
    Extract open skate events from the PDF table data.
    Args:
        tables (list): The table data extracted from the PDF page.
    Returns:
        list[Event]: A list of Event objects representing open skate sessions.
    """
    def extract_events_from_pdf_table(self, tables: list) -> list[Event]:
        events = []
        current_date = datetime.now()
        current_month_number = current_date.month
        for row in tables:
            for cell in row:
                if "Open Skate" in str(cell):
                    cell_lines = str(cell).split("\n")
                    for index, line in enumerate(cell_lines):
                        if "Open Skate" in line:
                            event_name = line.strip()
                            day_of_month_part = cell_lines[0]
                            time_string = cell_lines[index + 1]
                            start_time, end_time = self.parse_time_string(
                                time_string=time_string,
                                day_string=day_of_month_part,
                                month=current_month_number,
                                year=current_date.year
                            )
                            if "Vacation" in event_name:
                                cost = self.vacation_cost
                            else:
                                cost = self.standard_cost
                            event_notes = event_name.replace(':', '').strip()
                            event = self.create_event(cost, start_time, end_time, event_notes)
                            events.append(event)
                            # print(
                            #     f'Found event: {event_name} on day part: {current_month_number}/{day_of_month_part} at time: {time_string}')
                            ## Found event: Daytime Open Skate on day part: 12/18 at time: 11:30a-1:00p
                            ## Found event: Vacation Open Skate on day part: 12/26 at time: 11:30a - 1:00p
                            ## Found event: Sunday Open Skate: on day part: 12/28 at time: 1:30-3:00pm'
                            ## Found event: Vacation Open Skate on day part: 12/1/1 at time: 11:30a - 1:00p
        return events

    """
    Parse the time string and day string to create start and end datetime objects.
    Args:
        time_string (str): The time range string (e.g., "11:30a-1:00p").
        day_string (str): The day part string (e.g., "14" or "1/1").
        month (int): The current month number.
        year (int): The current year.
    Returns:
        tuple[datetime, datetime]: A tuple containing the start and end datetime objects.
    """
    def parse_time_string(self, time_string: str, day_string: str, month: int, year: int) -> tuple[datetime, datetime]:
        time_parts = time_string.replace(" ", "").split("-")
        start_time_str = time_parts[0]
        end_time_str = time_parts[1]

        if "/" in day_string:
            day_parts = day_string.split("/")
            day = int(day_parts[1])
            month = int(day_parts[0])
            if month <  month:
                year += 1
        else:
            day = int(day_string)

        start_time = self.convert_to_24_hour_format(start_time_str, day, month, year)
        end_time = self.convert_to_24_hour_format(end_time_str, day, month, year)

        return start_time, end_time

    """
    Create an Event object for the open skate session.
    Args:
        cost (Cost): The cost of the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        notes (str): Additional notes for the event.
    Returns:
        Event: An Event object representing the open skate session.
    """
    def create_event(self, cost:Cost, start_time:datetime, end_time:datetime, notes:str) -> Event:
        event = Event(
            event_type=EventType.OPEN_SKATE,
            arena=self.rosemount_ice_arena,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            notes=notes
        )
        return event

    """
    Convert a time string to a 24-hour format datetime object.
    Args:
        time_str (str): The time string (e.g., "11:30a", "1:00p").
        day (int): The day of the month.
        month (int): The month number.
        year (int): The year.
    Returns:
        datetime: A datetime object representing the time in 24-hour format.
    """
    @staticmethod
    def convert_to_24_hour_format(time_str: str, day: int, month: int, year: int) -> datetime:
        # Handle cases like "11:30a", "1:00p", "3:00pm"
        # Example time strings: "11:30a-1:00p", "1:30-3:00pm", "11:30a - 1:00p"
        # Assume "p" is pm
        # Assume "a" is am
        # Assume no suffix means pm

        if 'a' in time_str:
            time_str = time_str.replace('am', '').replace('a', '')
            hour_minute = datetime.strptime(time_str, "%I:%M")
        elif 'p' in time_str:
            time_str = time_str.replace('pm', '').replace('p', '')
            hour_minute = datetime.strptime(time_str, "%I:%M") + timedelta(hours=12)
        else:
            hour_minute = datetime.strptime(time_str, "%I:%M") + timedelta(hours=12)

        combined_datetime = datetime(year, month, day, hour_minute.hour, hour_minute.minute)
        return combined_datetime
