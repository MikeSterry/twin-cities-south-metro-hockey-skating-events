import json
from calendar import monthrange
from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from utils.Web_Utils import post_body_no_headers
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
        self.public_skating_cost = Cost(7.00)
        self.developmental_ice_cost = Cost(11.00)
        self.url = "https://burnsvillemn.gov/Admin/Facilities/Calendar/GetCalendarEvents"

    """
    Fetch events for the current from Burnsville Ice Center.
    If there are 4 or fewer days left in the month, also fetch events for the next month.
    Returns:
        list[Event]: A list of Event objects for the current and next month.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Burnsville events...')
        events = []

        current_date_epoch = self.get_epoch_for_today()
        next_week_epoch = self.get_epoch_for_next_week()

        try:
            post_body_text = f"start={current_date_epoch}&end={next_week_epoch}&calIDs=149"
            response = post_body_no_headers(self.url, post_body_text)
            json_response = json.loads(response)
            for item in json_response:
                if item['title'] is not None and item['title'] != '':
                    event_title = item['title']
                    start_time = self.convert_event_item_timestamp_to_datetime(item['start'])
                    end_time = self.convert_event_item_timestamp_to_datetime(item['end'])
                    if event_title == 'Public Skating':
                        event = self.create_event(EventType.OPEN_SKATE, self.public_skating_cost, start_time, end_time)
                        events.append(event)
                    if event_title == 'Burnsville Ice Center':
                        event = self.create_event(EventType.STICK_AND_PUCK, self.developmental_ice_cost, start_time, end_time)
                        events.append(event)
        except Exception as e:
            print(f'Error fetching Burnsville events: {e}')

        return events

    """
    Create an Event object.
    Args:
        event_type (EventType): The type of the event.
        cost (Cost): The cost associated with the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        notes (str): Additional notes for the event.
    Returns:
        Event: The created Event object.
    """
    def create_event(self, event_type: EventType, cost: Cost, start_time: datetime, end_time: datetime,
                     notes: str = "") -> Event:
        event = Event(
            event_type=event_type,
            arena=self.arena,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            notes=notes
        )
        return event

    """
    Get the Unix epoch timestamp for today's date at midnight.
    Returns:
        int: The Unix epoch timestamp for today's date at midnight.
    """
    def get_epoch_for_today(self):
        current_date = datetime.now()
        current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.convert_datetime_to_unix_timestamp(current_date)

    """
    Get the Unix epoch timestamp for the date one week from today at midnight.
    Returns:
        datetime: The Unix epoch timestamp for the date one week from today at midnight.
    """
    def get_epoch_for_next_week(self) -> datetime:
        current_date = datetime.now()
        current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        next_week = current_date + relativedelta(days=7)
        return self.convert_datetime_to_unix_timestamp(next_week)

    """
    Convert a datetime object to a Unix timestamp.
    Args:
        dt (datetime): The datetime object to convert.
    Returns:
        int: The Unix timestamp.
    """
    @staticmethod
    def convert_datetime_to_unix_timestamp(dt: datetime) -> int:
        return int(dt.timestamp())

    """
    Convert an event item timestamp string to a datetime object.
    Args:
        timestamp (str): The timestamp string to convert.
    Returns:
        datetime: The converted datetime object.
    """
    @staticmethod
    def convert_event_item_timestamp_to_datetime(timestamp: str) -> datetime:
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
