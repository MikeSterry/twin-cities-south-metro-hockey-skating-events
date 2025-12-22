from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from datetime import datetime, timedelta

class Edina():
    """
    Handler for Edina's ice skating events.
    """
    def __init__(self):
        address = Address(
            street = "",
            city = "",
            state = "",
            zip_code = ""
        )
        self.arena = Arena(
            name="",
            address=address
        )

    """
    Fetches events from Edina's ice skating schedule.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Edina events...')
        events = []
        return events