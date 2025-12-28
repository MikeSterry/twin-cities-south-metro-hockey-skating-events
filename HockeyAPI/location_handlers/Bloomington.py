from models.Address import Address
from models.Arena import Arena
from models.Cost import Cost
from models.Event import Event
from handlers.FinnlyConnectHandler import FinnlyConnectHandler

class Bloomington():
    """
    Handler for fetching events from Bloomington Ice Garden.
    """
    def __init__(self):
        address = Address(
            street="3600 W 98th St",
            city="Bloomington",
            state="MN",
            zip_code="55431"
        )
        arena = Arena(
            name="Bloomington Ice Garden",
            address=address
        )
        open_skate_cost = Cost(cost=5.00)
        developmental_hockey_cost = Cost(cost=12.00)
        url = "https://big.finnlyconnect.com/schedule/86"
        self.event_handler = FinnlyConnectHandler(arena, open_skate_cost, developmental_hockey_cost, url)

    """
    Fetches public skate and developmental hockey events from Bloomington Ice Garden.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Bloomington events...')
        events = []

        try:
            events = self.event_handler.get_events()
        except Exception as e:
            print(f'Error fetching Bloomington events: {e}')

        return events
