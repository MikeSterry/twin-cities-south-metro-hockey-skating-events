from multiprocessing.connection import address_type

from models.Arena import Arena
from models.Address import Address
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from datetime import datetime, timedelta

class AppleValley:
    """
    Initializes the Apple Valley Sports Arena open skate event handler.
    """
    def __init__(self) -> None:
        address = Address(
            street="14452 Hayes Rd",
            city="Apple Valley",
            state="MN",
            zip_code="55124"
        )
        self.arena = Arena(
            name="Apple Valley Sports Arena",
            address=address
        )

        self.event_type = EventType.OPEN_SKATE

        self.cost = Cost(cost=5.00)

        self.open_skate_start_date = datetime(datetime.now().year, 10, 19)
        self.open_skate_end_date = datetime(datetime.now().year + 1, 2, 22)

        self.OPEN_SKATE_START_HOUR = 15
        self.OPEN_SKATE_START_MINUTE = 30
        self.OPEN_SKATE_END_HOUR = 18
        self.OPEN_SKATE_END_MINUTE = 0

    """
    Fetches upcoming open skate events at Apple Valley Sports Arena.
    Returns:
        list[Event]: A list of Event objects representing upcoming open skate sessions.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Apple Valley events...')

        events = []

        try:
            current_date = datetime.now()
            start_date, end_date = self.get_start_and_end_dates()
            next_sunday = self.create_next_sunday_datetime(start_date)
            next_sunday_start_time = self.get_next_sunday_start_time(next_sunday)
            next_sunday_end_time = self.get_next_sunday_end_time(next_sunday)

            while next_sunday <= end_date and len(events) < 4:
                if next_sunday >= current_date:
                    event = Event(
                        event_type=self.event_type,
                        arena=self.arena,
                        start_time=next_sunday_start_time,
                        end_time=next_sunday_end_time,
                        cost=self.cost
                    )
                    events.append(event)
                next_sunday += timedelta(weeks=1)
        except Exception as e:
            print(f'Error fetching Apple Valley events: {e}')

        return events

    """
    Calculates the start time for the next Sunday open skate session.
    Args:
        from_date (datetime): The date from which to calculate the next Sunday.
    Returns:
        datetime: The start time of the next Sunday open skate session.
    """
    def get_next_sunday_start_time(self, from_date: datetime) -> datetime:
        return from_date.replace(hour=self.OPEN_SKATE_START_HOUR, minute=self.OPEN_SKATE_START_MINUTE, second=0,
                                 microsecond=0)

    """
    Calculates the end time for the next Sunday open skate session.
    Args:
        from_date (datetime): The date from which to calculate the next Sunday.
    Returns:
        datetime: The end time of the next Sunday open skate session.
    """
    def get_next_sunday_end_time(self, from_date: datetime) -> datetime:
        return from_date.replace(hour=self.OPEN_SKATE_END_HOUR, minute=self.OPEN_SKATE_END_MINUTE, second=0,
                                 microsecond=0)

    """
    Determines the start and end dates for the open skate season.
    Returns:
        tuple[datetime, datetime]: A tuple containing the start and end dates for the open skate season.
    """
    @staticmethod
    def get_start_and_end_dates() -> tuple[datetime, datetime]:
        current_date = datetime.now()
        start_date = datetime(current_date.year, 10, 19)
        end_date = datetime(current_date.year + 1, 2, 22)

        if current_date > end_date:
            start_date = datetime(current_date.year + 1, 10, 19)
            end_date = datetime(current_date.year + 2, 2, 22)

        return start_date, end_date

    """
    Creates a datetime object for the next Sunday from the given date.
    Args:
        datetime (datetime): The date from which to calculate the next Sunday.
    Returns:
        datetime: A datetime object representing the next Sunday.
    """
    @staticmethod
    def create_next_sunday_datetime(datetime: datetime) -> datetime:
        return datetime + timedelta((6 - datetime.weekday()) % 7)
