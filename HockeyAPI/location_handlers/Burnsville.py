from calendar import monthrange
from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from utils.Web_Utils import fetch_body, get_element_by_id, get_elements_by_tag_name, get_query_selector
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Burnsville:
    """
    Handler for Burnsville Ice Center events.
    """
    def __init__(self):
        address = Address(
            street="251 Civic Center Parkway",
            city="Burnsville",
            state="MN",
            zip_code="55337"
        )
        self.arena = Arena(
            name="Burnsville Ice Center",
            address=address
        )
        self.root_url = "https://www.burnsvillemn.gov"
        self.api_url = self.root_url + "/calendar.aspx?CID=99"

    """
    Fetch events for the current from Burnsville Ice Center.
    If there are 4 or fewer days left in the month, also fetch events for the next month.
    Returns:
        list[Event]: A list of Event objects for the current and next month.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Burnsville events...')
        events = []
        current_date = datetime.now()

        events_for_given_month = self.get_calendar_events_for_month(current_date)
        events.extend(events_for_given_month)

        if self.days_left_in_month() <= 3:
            next_month = current_date + relativedelta(months=1)
            events_for_next_month = self.get_calendar_events_for_month(next_month)
            events.extend(events_for_next_month)

        return events

    """
    1. Fetch the calendar page for the given month and year.
    2. Parse the HTML to find all event listings.
    3. For each event listing, extract the event name, link, date, and time.
    4. If the event name matches "Public Skating" or "Stick and Puck", create an Event object.
    5. Return a list of Event objects for the specified month.
    Args:
        datetime_object (datetime): A datetime object representing the month and year to fetch events for.
    Returns:
        list[Event]: A list of Event objects for the specified month.
    """
    def get_calendar_events_for_month(self, datetime_object: datetime) -> list[Event]:
        events = []

        try:
            check_year = datetime_object.year
            check_month = datetime_object.month
            current_calendar_url = self.api_url + f"&month={check_month}&year={check_year}"

            website_body = fetch_body(current_calendar_url)
            calendar_class_body = get_element_by_id(website_body, "CID99")
            if calendar_class_body:
                calendar_line_items = calendar_class_body.findAll("li")
                if len(calendar_line_items) > 0:
                    for calendar_line_item in calendar_line_items:
                        event_name = calendar_line_item.select("h3 > a > span")[0].get_text()
                        event_link = self.root_url + calendar_line_item.select("h3 > a")[0]["href"]
                        # start_date = calendar_line_item.find("span", {"itemprop": "startDate"}).get_text()
                        event_time_string = calendar_line_item.find("div", {"class": "date"}).get_text()
                        event_start_time, event_end_time = self.parse_event_time_string(event_time_string)

                        if event_name in ["Public Skating"]:
                            event_cost = self.get_cost_for_event(event_link)
                            event = self.create_event(event_type=EventType.OPEN_SKATE, cost=event_cost, start_time=event_start_time, end_time=event_end_time)
                            events.append(event)

                        elif event_name in ["Stick and Puck"]:
                            event_cost = self.get_cost_for_event(event_link)
                            event = self.create_event(event_type=EventType.STICK_AND_PUCK, cost=event_cost, start_time=event_start_time, end_time=event_end_time)
                            events.append(event)
        except Exception as e:
            print(f"Error fetching Burnsville events: {e}")

        return events

    """
    Create an Event object with the given parameters.
    Args:
        event_type (EventType): The type of the event.
        cost (Cost): The cost associated with the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
    Returns:
        Event: An Event object with the specified parameters.
    """
    def create_event(self, event_type:EventType, cost:Cost, start_time:datetime, end_time:datetime) -> Event:
        event = Event(
            event_type=event_type,
            arena=self.arena,
            start_time=start_time,
            end_time=end_time,
            cost=cost
        )
        return event

    """
    Parse the event time string to extract start and end datetime objects.
    Args:
        event_time_string (str): The event time string in the format "Month Day, Year, StartTime - EndTime".
    Returns:
        tuple[datetime, datetime]: A tuple containing the start and end datetime objects.
    """
    def parse_event_time_string(self, event_time_string: str) -> tuple[datetime, datetime]:
        month_and_day, year, time_part = event_time_string.split(",")[0], event_time_string.split(",")[1], event_time_string.split(",")[2]
        date_part = month_and_day + " " + year
        clean_time_part = time_part.encode("ascii", "ignore").decode("ascii")
        start_time_string, end_time_string = clean_time_part.split("-")[0], clean_time_part.split("-")[1]
        start_datetime_string = self.create_event_datetime(date_part, start_time_string.rstrip())
        end_datetime_string = self.create_event_datetime(date_part, end_time_string)
        return start_datetime_string, end_datetime_string

    """
    Combine date and time strings into a single datetime object.
    Args:
        date_string (str): The date string in the format "Month Day Year".
        time_string (str): The time string in the format "Hour:Minute AM/PM".
    Returns:
        datetime: A datetime object representing the combined date and time.
    """
    @staticmethod
    def create_event_datetime(date_string: str, time_string: str) -> datetime:
        date_object = datetime.strptime(date_string, "%B %d %Y")
        time_object = datetime.strptime(time_string, "%I:%M %p")
        combined_datetime = datetime(
            year=date_object.year,
            month=date_object.month,
            day=date_object.day,
            hour=time_object.hour,
            minute=time_object.minute
        )
        return combined_datetime

    """
    Fetch the cost information for a given event link.
    Args:
        event_link (str): The URL of the event page.
    Returns:
        Cost: A Cost object containing the cost and any notes.
    """
    @staticmethod
    def get_cost_for_event(event_link: str) -> Cost:
        event_link_body = fetch_body(event_link)
        cost_text = (get_element_by_id(event_link_body,
                                      "ctl00_ctl00_MainContent_ModuleContent_ctl00_ctl04_costDiv")
                     .get_text())
        # Todo: Parse cost text to clean things up
        return Cost(cost=8.00, notes=cost_text)

    @staticmethod
    def days_left_in_month() -> int:
        today = datetime.now()
        _, total_days = monthrange(today.year, today.month)
        return total_days - today.day