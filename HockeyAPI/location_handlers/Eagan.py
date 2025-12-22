from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from utils.Web_Utils import fetch_body
from ics import Calendar
from datetime import datetime, timedelta

class Eagan():
    """
    Eagan Civic Center event handler
    """
    def __init__(self):
        address = Address(
            street="3870 Pilot Knob Rd",
            city="Eagan",
            state="MN",
            zip_code="55122"
        )
        self.arena = Arena(
            name="Eagan Civic Center",
            address=address
        )
        self.root_url = "https://cityofeagan.com/index.php?option=com_dpcalendar&task=ical.download&id="
        self.civic_center_calendar_id = "934"
        self.civic_center_calendar_url = self.root_url + self.civic_center_calendar_id

    """
    Fetch events from Eagan Civic Center calendar
    Returns:
        list[Event]: List of Event objects
    """
    def get_events(self) -> list[Event]:
        events = []

        try:
            website_body = fetch_body(self.civic_center_calendar_url)
            calendar = Calendar(website_body)
            events = self.parse_ics_to_events(calendar)
        except Exception as e:
            print(f"Error fetching or parsing Eagan events: {e}")

        return events

    """
    Parse ICS calendar to extract events
    Args:
        icalendar: Calendar object
    Returns:
        list[Event]: List of Event objects
    """
    def parse_ics_to_events(self, calendar:Calendar) -> list[Event]:
        events = []
        print('Fetching Eagan Events...')
        for event in calendar.events:
            event_name = event.name.rstrip()
            event_description = event.description.rstrip()
            event_start = self.convert_to_datetime(event.begin.datetime)
            event_end = self.convert_to_datetime(event.end.datetime)
            if "Open Skate - All Ages" in event_description:

                cost = self.parse_cost_from_string(event_description)
                cost = Cost(cost=cost)

                event_notes = ""
                if event_description != "":
                    event_notes = event_description.replace('\n', ' - ')
                else:
                    event_notes = event_name

                event = self.create_event(
                    event_type=EventType.OPEN_SKATE,
                    arena=self.arena,
                    cost=cost,
                    start_time=event_start,
                    end_time=event_end,
                    notes=event_notes
                )
                events.append(event)

        return events

    """
    Parse cost from event description string
    Args:
        event_description (str): Event description
    Returns:
        float: Parsed cost as float
    """
    def parse_cost_from_string(self, event_description:str) -> float:
        cost = 0.0

        try:
            parsed_cost = float(self.parse_cost_from_description(event_description))
            cost = parsed_cost
        except ValueError:
            print("Could not convert string to float")

        return cost

    """
    Create Event object
    Args:
        event_type (EventType): Type of event
        arena (Arena): Arena where event takes place
        cost (Cost): Cost of the event
        start_time (datetime): Event start time
        end_time (datetime): Event end time
        notes (str): Additional notes about the event
    Returns:
        Event: Created Event object
    """
    @staticmethod
    def create_event(event_type:EventType, arena:Arena, cost:Cost, start_time:datetime, end_time:datetime, notes:str= "") -> Event:
        event = Event(
            event_type=event_type,
            arena=arena,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            notes=notes
        )
        return event

    """
    Parse cost from event description
    Args:
        description (str): Event description
    Returns:
        str: Parsed cost as string
    """
    @staticmethod
    def parse_cost_from_description(description:str) -> str:
        value = ""
        for line in description.splitlines():
            if "Admission" in line:
                value = line.split(":")[1].strip().split("&")[0].strip().split("/")[0].strip().replace("$", "")
                return value
        return value

    """
    Convert event datetime to standard datetime format
    Args
        event_datetime (datetime): Event datetime
    Returns:
        datetime: Standardized datetime object
    """
    @staticmethod
    def convert_to_datetime(event_datetime: datetime) -> datetime:
        return datetime(event_datetime.year, event_datetime.month, event_datetime.day, event_datetime.hour, event_datetime.minute)