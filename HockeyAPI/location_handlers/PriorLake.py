from models.Event import Event
from models.Address import Address
from models.Arena import Arena
from models.Cost import Cost
from enums.Event_Type import EventType

class PriorLake:

    def __init__(self):
        self.url = "https://www.dakotahsport.com/explore/ice-center/open-skate-adult-hockey"
        self.address: Address = Address(
            street="2100 Trail of Dreams",
            city="Prior Lake",
            state="MN",
            zip_code="55372"
        )
        self.arena: Arena = Arena(
            name="Dakotah Ice Center",
            address=self.address,
            notes="Open Skate schedule is not published online yet; which is odd considering the size of the arena..."
        )
        self.open_skate_cost: Cost = Cost(5)
        self.event_type = EventType.OPEN_SKATE
        self.EVENT_NOTES = "Open Skate is free for members."

        """
        Adult open hockey is open to players ages 18+
        Going to skip it since we've been focusing on youth hockey
        """
        self.adult_hockey: Cost = Cost(7)

    """
    Fetches public skate events from Prior Lake's Dakotah Ice Center.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        return []