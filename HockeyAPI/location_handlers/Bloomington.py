import json

from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from datetime import datetime, timedelta
from utils.Web_Utils import fetch_body, get_query_selector

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

        self.arena = Arena(
            name="Bloomington Ice Garden",
            address=address
        )

        self.open_skate_cost = Cost(cost=5.00)
        self.developmental_hockey_cost = Cost(cost=12.00)

        self.url = "https://big.finnlyconnect.com/schedule/86"

    """
    Fetches public skate and developmental hockey events from Bloomington Ice Garden.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Bloomington events...')
        events = []

        try:
            online_schedule_json = self.get_json_objects_from_site()

            for online_schedule in online_schedule_json:
                # print('Online Schedule: {}'.format(online_schedule))
                facility_name = online_schedule['FacilityName']
                event_name = online_schedule['AccountName']
                start_time = online_schedule['EventStartTime']
                end_time = online_schedule['EventEndTime']
                start_datetime_object = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
                end_datetime_object = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

                if event_name == "Developmental Ice'":
                    arena = self.arena
                    arena.set_notes(facility_name)
                    event_notes = event_name + " - " + facility_name
                    event = self.create_event(EventType.STICK_AND_PUCK, arena, self.developmental_hockey_cost, start_datetime_object, end_datetime_object, event_notes)
                    events.append(event)
                elif event_name == "Open Skating":
                    arena = self.arena
                    arena.set_notes(facility_name)
                    event_notes = event_name + " - " + facility_name
                    event = self.create_event(EventType.OPEN_SKATE, arena, self.open_skate_cost, start_datetime_object, end_datetime_object, event_notes)
                    events.append(event)
        except Exception as e:
            print(f'Error fetching Bloomington events: {e}')

        return events

    """
    Fetches the JSON objects containing the online schedule from the Bloomington Ice Garden website.
    Returns:
        dict: A dictionary containing the online schedule JSON data.
    """
    def get_json_objects_from_site(self) -> dict:
        online_schedule_json = {}

        website_body = fetch_body(self.url)
        script_bodies = get_query_selector(website_body, 'script')
        for script_body in script_bodies:
            script_string = str(script_body.string)
            if "eventTypeResourceList" in script_string:
                for line in script_string.splitlines():
                    if "_onlineScheduleList = " in line:
                        online_schedule_json = self.get_online_schedule_json(line)

        return online_schedule_json

    """
    Creates an Event object with the provided details.
    Args:
        event_type (EventType): The type of the event.
        arena (Arena): The arena where the event takes place.
        cost (Cost): The cost associated with the event.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        notes (str, optional): Additional notes about the event. Defaults to "".
    Returns:
        Event: An Event object with the specified details.
    """
    @staticmethod
    def create_event(event_type:EventType, arena:Arena, cost:Cost, start_time:datetime, end_time:datetime, notes:str= "") -> Event:
        event = Event(
            event_type=event_type,
            arena=arena,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            notes=notes
        )
        return event

    """
    Extracts the online schedule JSON from the provided string.
    Args:
        online_schedule_list_string (str): The string containing the online schedule list.
    Returns:
        dict: A dictionary containing the online schedule JSON data.
    """
    def get_online_schedule_json(self, online_schedule_list_string) -> dict:
        return self.convert_string_to_json(online_schedule_list_string
                                      .split(' = ')[1]
                                      .rstrip(';'))

    """
    Converts a JSON string to a dictionary.
    Args:
        json_string (str): The JSON string to be converted.
    Returns:
        dict: A dictionary representation of the JSON string.
    """
    @staticmethod
    def convert_string_to_json(json_string) -> dict:
        return json.loads(json_string)