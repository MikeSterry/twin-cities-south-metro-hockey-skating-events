from models.Event import Event
from models.Address import Address
from models.Arena import Arena
from models.Cost import Cost
from handlers.FinnlyConnectHandler import FinnlyConnectHandler

class Skakopee:

    def __init__(self):
        address: Address = Address(
            street="1225 Fuller St S",
            city="Shakopee",
            state="MN",
            zip_code="55379"
        )
        arena: Arena = Arena(
            name="Shakopee Ice Center",
            address=address
        )
        open_skate_cost = Cost(cost=6.00)
        developmental_hockey_cost = Cost(cost=6.00)
        url = "https://shakopeeice.finnlyconnect.com/schedule/137"

        self.event_handler = FinnlyConnectHandler(arena, open_skate_cost, developmental_hockey_cost, url)

    """
    Fetches public skate and developmental hockey events from Shakopee Ice Arena.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Shakopee events...')
        events = []

        try:
            events = self.event_handler.get_events()
        except Exception as e:
            print(f'Error fetching Shakopee events: {e}')

        return events
