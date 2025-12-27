from datetime import datetime, timedelta
from models.Event import Event
from location_handlers.AppleValley import AppleValley
from location_handlers.Burnsville import Burnsville
from location_handlers.Lakeville import Lakeville
from location_handlers.Eagan import Eagan
from location_handlers.Rosemount import Rosemount
from location_handlers.Bloomington import Bloomington
from location_handlers.Edina import Edina
from location_handlers.InverGroveHeights import InverGroveHeights
from location_handlers.Richfield import Richfield
from location_handlers.SouthStPaul import SouthStPaul

class EventHandler:
    """
    Handles event processing including filtering, sorting, and removing duplicates.
    """

    def __init__(self):
        self.apple_valley_handler = AppleValley()
        self.burnsville_handler = Burnsville()
        self.lakeville_handler = Lakeville()
        self.eagan_handler = Eagan()
        self.rosemount_handler = Rosemount()
        self.bloomington_handler = Bloomington()
        self.edina_handler = Edina()
        self.inver_grove_heights_handler = InverGroveHeights()
        self.richfield_handler = Richfield()
        self.south_st_paul_handler = SouthStPaul()

    def get_events(self) -> list[Event]:
        events = self.get_location_events()
        print(f'Total events fetched: {len(events)}')
        filtered_events = self.filter_events_next_24_hours(events)
        non_duplicate_events = self.remove_duplicates(filtered_events)
        print(f'Total events after filtering: {len(non_duplicate_events)}')
        ordered_events = self.sort_events(non_duplicate_events)

        if ordered_events:
            events_json = []
            for event in ordered_events:
                event_data = {
                    "arena": {
                        "name": event.arena.name,
                        "address": {
                            "street": event.arena.address.street,
                            "city": event.arena.address.city,
                            "state": event.arena.address.state,
                            "zip_code": event.arena.address.zip_code
                        },
                        "notes": event.arena.notes
                    },
                    "event_type": event.event_type.value,
                    "start_time": event.start_time.strftime("%Y-%m-%d %H:%M"),
                    "end_time": event.end_time.strftime("%Y-%m-%d %H:%M"),
                    "notes": event.notes,
                    "cost": {
                        "cost": event.cost.get_cost()
                    }
                }
                events_json.append(event_data)
            return events_json
        else:
            return []

    def get_location_events(self) -> list[Event]:
        events = []
        events.extend(self.apple_valley_handler.get_events())
        events.extend(self.burnsville_handler.get_events())
        events.extend(self.lakeville_handler.get_events())
        events.extend(self.eagan_handler.get_events())
        events.extend(self.rosemount_handler.get_events())
        events.extend(self.bloomington_handler.get_events())
        events.extend(self.inver_grove_heights_handler.get_events())
        events.extend(self.richfield_handler.get_events())
        events.extend(self.south_st_paul_handler.get_events())

        # events.extend(edina_handler.get_events())                 # Todo: Finish Edina handler
        # Farmington handler not implemented yet
        # Mistic Lake handler not implemented yet
        # Shakopee handler not implemented yet
        # Highland handler not implemented yet
        # Pleasant handler not implemented yet
        # West St Paul handler not implemented yet

        return events

    """
    Filter events by date range (optional) - next 24 hours
    """

    def filter_events_next_24_hours(self, events: list[Event]) -> list[Event]:
        now = datetime.now()
        next_24_hours = now + timedelta(hours=48)
        return self.filter_events_by_date_range(events, now, next_24_hours)

    """
    Filter events by date range
    """

    @staticmethod
    def filter_events_by_date_range(events: list[Event], start_date, end_date) -> list[Event]:
        filtered_events = []
        for event in events:
            # print(f'Event start time: {event.start_time}, Filter range: {start_date} - {end_date}')
            if start_date <= event.start_time <= end_date:
                # print(f'{event.start_time} is greater than {start_date} and less than {end_date}')
                filtered_events.append(event)
        return filtered_events

    """
    Sort events by start time
    """

    @staticmethod
    def sort_events(events: list[Event]) -> list[Event]:
        return sorted(events, key=lambda event: event)

    """
    Remove duplicate events
    Args:
        events (list[Event]): List of events to remove duplicates from.
    Returns:
        list[Event]: List of events with duplicates removed.
    """

    @staticmethod
    def remove_duplicates(events: list[Event]) -> list[Event]:
        return list(dict.fromkeys(events))