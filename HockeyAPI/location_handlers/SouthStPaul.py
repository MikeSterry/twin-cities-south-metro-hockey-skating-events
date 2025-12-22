from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from utils.Web_Utils import fetch_body, get_query_selector


class SouthStPaul():
    """
    Handler for South St Paul Doug Woog Arena open skate events.
    """
    def __init__(self):
        address = Address(
            street = "141 6th St S",
            city = "South St Paul",
            state = "MN",
            zip_code = "55075"
        )
        self.arena = Arena(
            name="Doug Woog Arena",
            address=address,
            notes="$5 per person, $20 punch pass - 5 open skate sessions, $40 punch pass - 10 open skate sessions"
        )

        self.cost = Cost(5.00)

        self.root_url = "https://www.southstpaul.org/calendar.aspx?CID=26,27"

    """
    Fetch and parse open skate events from the South St Paul calendar.
    Returns:
        list[Event]: A list of Event objects representing open skate sessions.
    """
    def get_events(self) -> list[Event]:
        print('Fetching South St Paul events...')
        events = []

        try:
            current_date = datetime.now()
            events = self.get_events_from_calendar(current_date)
            next_month = current_date + relativedelta(months=1)
            events.extend(self.get_events_from_calendar(next_month))
        except Exception as e:
            print(f"An error occurred while fetching South St Paul events: {e}")

        return events

    """
    Parse events from the South St Paul calendar for a given month.
    Args:
        current_date (datetime): The date representing the month to fetch events for.
    Returns:
        list[Event]: A list of Event objects for the specified month.
    """
    def get_events_from_calendar(self, current_date: datetime) -> list[Event]:
        events = []

        try:
            current_month = current_date.month
            current_year = current_date.year
            website_body = fetch_body(self.root_url + f"&month={current_month}&year={current_year}")
            calendar_body = get_query_selector(website_body, '.monthItem ')
            for calendar_item in calendar_body:
                event_name = calendar_item.select("a > span")[0].get_text()
                event_time_string = calendar_item.select(".tooltipInner")[0].select("div > dl > dd")[0].get_text()
                event_date_string = calendar_item.select(".tooltipInner")[0].select("a")[0].get('href')
                event_date = self.parse_event_date_string(event_date_string)
                event_start_time, event_end_time = self.parse_event_time_string(event_date, event_time_string)
                # print(f'Found event name: {event_name} from: {event_start_time} to {event_end_time}')
                if event_name in ["Open Skate Session"]:
                    event = self.create_event(event_type=EventType.OPEN_SKATE, start_time=event_start_time, end_time=event_end_time)
                    events.append(event)
                elif event_name in ["Stick & Puck Session", "Stick and Puck Session"]:
                    event = self.create_event(event_type=EventType.STICK_AND_PUCK, start_time=event_start_time, end_time=event_end_time)
                    events.append(event)
        except Exception as e:
            print(f"An error occurred while parsing South St Paul calendar events: {e}")

        return events

    """
    Create an Event object.
    Args:
        event_type (EventType): The type of the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        notes (str): Additional notes for the event.
    Returns:
        Event: An Event object representing the open skate session.
    """
    def create_event(self, event_type: EventType, start_time: datetime, end_time: datetime, notes: str = "") -> Event:
        event = Event(
            event_type=event_type,
            arena=self.arena,
            start_time=start_time,
            end_time=end_time,
            cost=self.cost,
            notes=notes
        )
        return event

    """
    Parse the event date string to extract the date.
    Args:
        event_date_string (str): The event date string from the calendar link.
    Returns:
        datetime: A datetime object representing the event date.
    """
    @staticmethod
    def parse_event_date_string(event_date_string: str) -> datetime:
        # Example input: "/Calendar.aspx?EID=4411&month=12&year=2025&day=28&calType=0"
        # Return a datetime.date object
        # print(f'Parsing event date string: {event_date_string}')
        query_params = event_date_string.split("?")[1].split("&")
        day = 1
        month = 1
        year = 2000
        for param in query_params:
            key, value = param.split("=")
            if key == "day":
                day = int(value)
            elif key == "month":
                month = int(value)
            elif key == "year":
                year = int(value)
        event_date = datetime(year, month, day)
        return event_date

    """
    Parse the event time string to extract start and end times.
    Args:
        event_date (datetime): The date of the event.
        event_time_string (str): The time range string (e.g., "12:30 PM - 2:00 PM").
    Returns:
        tuple[datetime, datetime]: A tuple containing the start and end datetime objects.
    """
    @staticmethod
    def parse_event_time_string(event_date: str, event_time_string: str) -> tuple[datetime, datetime]:
        # print(f'Parsing event time string: {event_time_string}')
        # Example input: "12:30 PM - 2:00 PM"
        time_parts = event_time_string.split("-")
        start_time_str = time_parts[0].strip()
        # print(f'Start time string: {start_time_str}')
        end_time_str = time_parts[1].strip()
        # print(f'End time string: {end_time_str}')

        today_date = event_date.date()
        start_time = datetime.strptime(f"{today_date} {start_time_str}", "%Y-%m-%d %I:%M %p")
        end_time = datetime.strptime(f"{today_date} {end_time_str}", "%Y-%m-%d %I:%M %p")

        return start_time, end_time