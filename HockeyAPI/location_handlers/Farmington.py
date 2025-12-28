from datetime import datetime, timedelta

from enums.Event_Type import EventType
from models.Address import Address
from models.Arena import Arena
from models.Cost import Cost
from models.Event import Event
from enums.Week_Day import WeekDay
import utils.Holidays

"""
Handler for Farmington Schmitz-Maki Arena open skate events.

Worth noting that Farmington has a bunch of calendars and pages for this same arena. The most recent up to date one 
states that they offer both Open Hockey and Stick and Puck and that both are year round. However, the only calendar that
is actually populated with events is the one that shows Open Skate on Sundays from October to March, which is what this 
handler implements.

Also worth nothing that although the calendar shows events from October to March, the arena website states that Open Skate
is offered year round on Wednesdays and Sundays. However, since no calendar exists, I really can't tell if the times changes
throughout the year or if there are any holidays or special events that would cancel open skate sessions.

They also show pricing for Stick and Puck, but they don't show any actual times for those events. So I'm going to play
it safe and assume that only Open Skate is offered until I can find more information.

What I do know is there are a HUGE hockey community in Farmington and they definitely struggle to find ice time. I know 
this because they buy ice time from neighboring cities and rent out entire ice sheets for practices and scrimmages. 
This leads me to believe that their arena probably doesn't have a lot of opening for public events. So I'm going to limit
things to just Open Skate.
"""
class Farmington:
    def __init__(self):
        address = Address(
            street="114 West Spruce Street",
            city="Farmington",
            state="MN",
            zip_code="55024"
        )
        self.arena = Arena(
            name="Schmitz-Maki Arena",
            address=address,
            notes="Offers skate rentals - $6 a pair"
        )

        self.event_type = EventType.OPEN_SKATE
        self.EVENT_NOTES = "The open skate daily admission per-person rate is $6. Punch card/10 is $54."

        self.cost = Cost(cost=6.00)

        self.WEDNESDAY_OPEN_SKATE_START_HOUR = 11
        self.WEDNESDAY_OPEN_SKATE_START_MINUTE = 00
        self.WEDNESDAY_OPEN_SKATE_END_HOUR = 12
        self.WEDNESDAY_OPEN_SKATE_END_MINUTE = 30

        self.SUNDAY_OPEN_SKATE_START_HOUR = 13
        self.SUNDAY_OPEN_SKATE_START_MINUTE = 30
        self.SUNDAY_OPEN_SKATE_END_HOUR = 15
        self.SUNDAY_OPEN_SKATE_END_MINUTE = 00

        self.DAYS_TO_FETCH = 30

    """
    Fetches upcoming open skate events at Arena.
    Returns:
        list[Event]: A list of Event objects representing upcoming open skate sessions.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Farmington events...')
        events = []

        try:
            wednesday_events = self.create_wednesday_events()
            sunday_events = self.create_sunday_events()
            events.extend(wednesday_events)
            events.extend(sunday_events)
        except Exception as e:
            print(f"An error occurred while fetching Farmington events: {e}")

        return events

    """
    Create open skate events for Wednesdays.
    Returns:
        list[Event]: A list of Event objects for Wednesdays.
    """
    def create_wednesday_events(self) -> list[Event]:
        events = []
        wednesdays = self.get_wednesdays()
        filtered_wednesdays = self.filter_holiday_events(wednesdays)

        for wednesday in filtered_wednesdays:
            start_time = wednesday.replace(hour=self.WEDNESDAY_OPEN_SKATE_START_HOUR,
                                           minute=self.WEDNESDAY_OPEN_SKATE_START_MINUTE, second=0, microsecond=0)
            end_time = wednesday.replace(hour=self.WEDNESDAY_OPEN_SKATE_END_HOUR,
                                         minute=self.WEDNESDAY_OPEN_SKATE_END_MINUTE, second=0, microsecond=0)
            event = self.create_event(start_time, end_time)
            events.append(event)

        return events
    """
    Create open skate events for Sundays.
    Returns:
        list[Event]: A list of Event objects for Sundays.
    """
    def create_sunday_events(self) -> list[Event]:
        events = []
        sundays = self.get_sundays()
        filtered_sundays = self.filter_holiday_events(sundays)

        for sunday in filtered_sundays:
            start_time = sunday.replace(hour=self.SUNDAY_OPEN_SKATE_START_HOUR,
                                        minute=self.SUNDAY_OPEN_SKATE_START_MINUTE, second=0, microsecond=0)
            end_time = sunday.replace(hour=self.SUNDAY_OPEN_SKATE_END_HOUR,
                                      minute=self.SUNDAY_OPEN_SKATE_END_MINUTE, second=0, microsecond=0)
            event = self.create_event(start_time, end_time)
            events.append(event)

        return events
    """
    Create an Event object with the given parameters.
    Args:
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
    Returns:
        Event: An Event object with the specified parameters.
    """
    def create_event(self, start_time: datetime, end_time: datetime) -> Event:
        event = Event(
            event_type=self.event_type,
            arena=self.arena,
            start_time=start_time,
            end_time=end_time,
            cost=self.cost,
            notes=self.EVENT_NOTES
        )
        return event

    """
    Get all Sundays in the next specified number of days.
    Returns:
        list[datetime]: A list of datetime objects representing Sundays.
    """
    def get_sundays(self) -> list[datetime]:
        next_x_days = self.get_list_of_days(self.DAYS_TO_FETCH)
        sundays = self.get_specific_days_from_datetime_list(next_x_days, "Sunday")
        return sundays

    """
    Get all Wednesdays in the next specified number of days.
    Returns:
        list[datetime]: A list of datetime objects representing Wednesdays.
    """
    def get_wednesdays(self) -> list[datetime]:
        next_x_days = self.get_list_of_days(self.DAYS_TO_FETCH)
        wednesdays = self.get_specific_days_from_datetime_list(next_x_days, "Wednesday")
        return wednesdays

    """
    Filter out dates that fall on holidays.
    Args:
        dates (list[datetime]): List of datetime objects to filter.
    Returns:
        list[datetime]: Filtered list of datetime objects excluding holidays.
    """
    @staticmethod
    def filter_holiday_events(dates: list[datetime]) -> list[datetime]:
        for date in dates:
            if utils.Holidays.is_holiday(date):
                dates.remove(date)
        return dates

    """
    Generate a list of datetime objects for the next specified number of days.
    Args:
        number_of_days (int): The number of days to generate.
    Returns:
        list[datetime]: A list of datetime objects for the next specified number of days.
    """
    @staticmethod
    def get_list_of_days(number_of_days: int) -> list[datetime]:
        list_of_days = []
        current_date = datetime.now()
        for i in range(number_of_days):
            list_of_days.append(current_date + timedelta(days=i))
        return list_of_days

    """
    Get specific days from a list of datetime objects.
    Args:
        datetime_list (list[datetime]): List of datetime objects.
        target_day_name (str): The name of the target day (e.g., "Sunday", "Wednesday").
    Returns:
        list[datetime]: A list of datetime objects that match the target day.
    """
    @staticmethod
    def get_specific_days_from_datetime_list(datetime_list: list[datetime], target_day_name: str) -> list[datetime]:
        specific_days = []
        for date in datetime_list:
            if date.weekday() == WeekDay.get_weekday(target_day_name).value:
                specific_days.append(date)
        return specific_days