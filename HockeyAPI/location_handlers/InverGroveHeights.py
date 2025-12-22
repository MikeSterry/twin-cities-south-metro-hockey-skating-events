import json

from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from datetime import datetime, timedelta
from utils.Web_Utils import post_body


class InverGroveHeights():
    """
    Handler for Inver Grove Heights ice skating events.
    """
    def __init__(self):
        address = Address(
            street = "8055 Barbara Ave",
            city = "Inver Grove Heights",
            state = "MN",
            zip_code = "55077"
        )
        self.arena = Arena(
            name="Veterans Memorial Community Center",
            address=address
        )

        self.cost = Cost(7.00)
        self.developmental_ice_cost = Cost(11.00)

        self.url = "https://anc.apm.activecommunities.com/igh/rest/onlinecalendar/multicenter/events?locale=en-US"

        self.post_body = """{
            "calendar_id": 8,
            "center_ids": [
                2
            ],
            "display_all": 0,
            "search_start_time": "",
            "search_end_time": "",
            "facility_ids": [],
            "activity_category_ids": [],
            "activity_sub_category_ids": [],
            "activity_ids": [],
            "activity_min_age": null,
            "activity_max_age": null,
            "event_type_ids": []
        }"""

    """
    Fetches and processes Inver Grove Heights ice skating events.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Inver Grove Heights events...')
        events = []

        try:
            response = post_body(self.url, self.post_body)
            # print(f'Inver Grove Heights response: {response}')
            json_response = json.loads(response)
            json_events = json_response['body']['center_events'][0]['events']
            for json_event in json_events:
                event_name = json_event['title']
                event_start_time = datetime.strptime(json_event['start_time'], "%Y-%m-%d %H:%M:%S")
                event_end_time = datetime.strptime(json_event['end_time'], "%Y-%m-%d %H:%M:%S")
                rink_name = json_event['facilities'][0]['facility_name'] if json_event['facilities'] else ""
                notes = rink_name
                event_description = json_event['description'] if json_event['description'] else ""
                if event_description != "":
                    notes += f" - {event_description}"

                # print(f'Processing Richfield event: {event_name} from {event_start_time} to {event_end_time}')

                if "Open Public Skating" in event_name:
                    event_type = EventType.OPEN_SKATE
                    arena = self.arena
                    arena.set_notes(rink_name)
                    event = self.create_event(event_type, arena, self.cost, event_start_time, event_end_time, notes)
                    events.append(event)
                elif "Stick & Puck" in event_name:
                    event_type = EventType.STICK_AND_PUCK
                    arena = self.arena
                    arena.set_notes(rink_name)
                    event = self.create_event(event_type, arena, self.cost, event_start_time, event_end_time, notes)
                    events.append(event)
                elif "Developmental Ice" in event_name:
                    event_type = EventType.STICK_AND_PUCK
                    arena = self.arena
                    arena.set_notes(rink_name)
                    event = self.create_event(event_type, arena, self.developmental_ice_cost, event_start_time, event_end_time, notes)
                    events.append(event)
        except Exception as e:
            print(f'Error fetching Inver Grove Heights events: {e}')

        return events

    """
    Creates an Event object.
    Args:
        event_type (EventType): The type of the event.
        arena (Arena): The arena where the event takes place.
        cost (Cost): The cost associated with the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        notes (str, optional): Additional notes about the event. Defaults to "".
    Returns:
        Event: The created Event object.
    """
    @staticmethod
    def create_event(event_type: EventType, arena: Arena, cost: Cost, start_time: datetime, end_time: datetime,
                     notes: str = "") -> Event:
        event = Event(
            event_type=event_type,
            arena=arena,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            notes=notes
        )
        return event