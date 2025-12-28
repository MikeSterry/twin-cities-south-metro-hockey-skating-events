from models.Address import Address
from models.Arena import Arena
from models.Cost import Cost
from models.Event import Event
from handlers.FinnlyConnectHandler import FinnlyConnectHandler

class Edina():
    """
    Handler for Edina's ice skating events.
    Edina only offers public skating. Developmental hockey is a full sheet reservation only.
    """
    def __init__(self):
        address = Address(
            street="7501 Ikola Way,",
            city="Edina",
            state="MN",
            zip_code="55439"
        )
        self.ARENA_NOTES = "Edina only offers public skating. Developmental hockey is a full sheet reservation only."
        arena = Arena(
            name="Braemar Arena",
            address=address,
            notes=self.ARENA_NOTES
        )
        open_skate_cost = Cost(cost=7.00)
        developmental_hockey_cost = Cost(cost=7.00)
        open_skate_name = "Open Skate"
        developmental_hockey_name = "Developmental Ice"
        url = "https://braemararenaandfield.finnlyconnect.com/schedule/164"
        self.event_handler = FinnlyConnectHandler(arena, open_skate_cost, developmental_hockey_cost, url,
                                                  open_skate_name, developmental_hockey_name)

    """
    Fetches public skate and developmental hockey events from Edina Braemar Arena.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Edina events...')
        fixed_events = []

        try:
            events = self.event_handler.get_events()
            fixed_events = self.strip_arena_notes(events)
        except Exception as e:
            print(f'Error fetching Edina events: {e}')

        return fixed_events

    """
    Edina adds the wrong rink notes via the facility name for each event's Arena in FinnlyConnect.
    This method strips those Arena notes from each event and updates them with the correct Arena notes.
    The correct rink are included in the event notes
    Args:
        events (list[Event]): List of Event objects
    Returns:
        list[Event]: List of Event objects with stripped notes
    """
    def strip_arena_notes(self, events: list[Event]) -> list[Event]:
        new_events = []
        for event in events:
            event.arena.notes = self.ARENA_NOTES
            new_events.append(event)
        return new_events
