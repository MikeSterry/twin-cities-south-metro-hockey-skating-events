import json
from calendar import monthrange
from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from utils.Web_Utils import post_body
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Burnsville:
    """
    Handler for Burnsville Ice Center events.

    Couple Notes:
        The current API does not return Stick and Puck events.
        I could go directly to the Ice Arena ASPX calendar page, but it's sooooo slow...
        That said, I do know that both events happen at the same time but only during on week days.
        Public skating events on Sundays will NOT coincide with Stick and Puck.
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
            post_body_text = '{"start": ' + str(current_date_epoch) + ',"end": ' + str(next_week_epoch) + ',"calIDs": 149}'
            response = post_body(self.url, post_body_text)
            json_response = json.loads(response)
            events.extend(self.create_events_from_json_response(json_response))
        except Exception as e:
            print(f'Error fetching Burnsville events: {e}')

        return events

    """
    Create Event objects from the JSON response.
    Args:
        json_response (list): The JSON response containing event data.
    Returns:
        list[Event]: A list of Event objects created from the JSON response.
    """
    def create_events_from_json_response(self, json_response) -> list[Event]:
        events = []
        for item in json_response:
            if item['title'] is not None and item['title'] != '':
                event_title = item['title']
                start_time = self.convert_event_item_timestamp_to_datetime(item['start'])
                end_time = self.convert_event_item_timestamp_to_datetime(item['end'])
                if event_title == 'Public Skating':
                    event = self.create_event(EventType.OPEN_SKATE, self.public_skating_cost, start_time, end_time)
                    events.append(event)
                    if not self.is_date_sunday(start_time):
                        event = self.create_event(EventType.STICK_AND_PUCK, self.developmental_ice_cost, start_time,
                                              end_time)
                    events.append(event)
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
    @staticmethod
    def get_epoch_for_today() -> int:
        start_of_today = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return int(start_of_today.timestamp())

    """
    Get the Unix epoch timestamp for the date one week from today at midnight.
    Returns:
        int: The Unix epoch timestamp for the date one week from today at midnight.
    """
    @staticmethod
    def get_epoch_for_next_week() -> int:
        start_of_today = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        next_week = start_of_today + relativedelta(days=7)
        return int(next_week.timestamp())

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

    """
    Check if a given date is a Sunday.
    Args:
        date (datetime): The date to check.
    Returns:
        bool: True if the date is a Sunday, False otherwise.
    """
    @staticmethod
    def is_date_sunday(date: datetime) -> bool:
        return date.weekday() == 6
