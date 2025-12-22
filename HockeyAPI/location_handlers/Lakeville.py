import json

from models.Address import Address
from models.Arena import Arena
from enums.Event_Type import EventType
from models.Cost import Cost
from models.Event import Event
from utils.Web_Utils import fetch_body, get_query_selector
from datetime import datetime


class Lakeville:
    """
    Handler for Lakeville public skate and stick & puck events.
    """
    def __init__(self):
        self.root_url = "https://lakevillepublicopenskate.finnlyconnect.com/schedule/132"

        self.cost = Cost(10.00)

        ames_arena_address = Address(
            street = "19900 Ipava Ave",
            city = "Lakeville",
            state = "MN",
            zip_code = "55044"
        )
        self.lakeview_bank_rink = Arena(
            name="Ames Arena - Lakeview Bank Rink",
            address=ames_arena_address,
        )

        self.genz_ryan_rink = Arena(
            name="Ames Arena - Lakeview Bank Rink",
            address=ames_arena_address
        )

        hasse_arena_address = Address(
            street = "8525 215th St W",
            city = "Lakeville",
            state = "MN",
            zip_code = "55044"
        )
        self.hasse_arena = Arena(
            name="Hasse Arena",
            address=hasse_arena_address
        )

    """
    Fetches public skate and stick & puck events from Lakeville's online schedule.
    Returns:
        list[Event]: A list of Event objects representing the fetched events.
    """
    def get_events(self) -> list[Event]:
        print('Fetching Lakeville events...')
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
                event_notes = online_schedule['AccountName'] + " - " + online_schedule['ScheduleNotes']

                if event_name == "PUBLIC STICK & PUCK - ALL AGES":
                    arena = self.create_arena(facility_name)
                    event = self.create_event(EventType.STICK_AND_PUCK, arena, self.cost, start_datetime_object, end_datetime_object, event_notes)
                    events.append(event)
                elif event_name == "PUBLIC OPEN SKATING":
                    arena = self.create_arena(facility_name)
                    event = self.create_event(EventType.OPEN_SKATE, arena, self.cost, start_datetime_object, end_datetime_object, event_notes)
                    events.append(event)
        except Exception as e:
            print(f'Error fetching Lakeville events: {e}')

        return events

    """
    Extracts JSON objects from the Lakeville online schedule webpage.
    Returns:
        dict: A dictionary containing the extracted JSON objects.
    """
    def get_json_objects_from_site(self) -> dict:
        facility_json = {}
        event_type_json = {}
        online_schedule_json = {}

        website_body = fetch_body(self.root_url)
        script_bodies = get_query_selector(website_body, 'script')
        for script_body in script_bodies:
            script_string = str(script_body.string)
            if "eventTypeResourceList" in script_string:
                for line in script_string.splitlines():
                    # if "_facilityList = " in line:
                    #     facility_json = get_facility_json(line)
                    # if "_eventTypeList = " in line:
                    #     event_type_json = get_event_type_json(line)
                    if "_onlineScheduleList = " in line:
                        online_schedule_json = self.get_online_schedule_json(line)

        return online_schedule_json

    """
    Creates an Arena object based on the facility name.
    Args:
        facility_name (str): The name of the facility.
    Returns:
        Arena: The corresponding Arena object.
    """
    def create_arena(self, facility_name:str) -> Arena:
        if facility_name == "1.Ames Arena-Lakeview Bank Rink":
            return self.lakeview_bank_rink
        elif facility_name == "2.Ames Arena-Genz-Ryan Rink":
            return self.genz_ryan_rink
        elif facility_name == "3.Hasse Arena":
            return self.hasse_arena
        else:
            return Arena(
                name=facility_name,
                address="",
                notes="Unknown rink facility"
            )

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
        Event: The created Event object.
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
    Converts a JSON string to a dictionary.
    Args:
        json_string (str): The JSON string to convert.
    Returns:
        dict: The converted dictionary.
    """
    @staticmethod
    def convert_string_to_json(json_string: str) -> dict:
        return json.loads(json_string)

    """
    Extracts the online schedule JSON from the provided string.
    Args:
        online_schedule_list_string (str): The string containing the online schedule JSON.
    Returns:
        dict: The extracted online schedule JSON.
    """
    def get_online_schedule_json(self, online_schedule_list_string: str) -> dict:
        return self.convert_string_to_json(online_schedule_list_string.split(' = ')[1].rstrip(';'))

    """
    Extracts the event type JSON from the provided string.
    Args:
        event_type_list_string (str): The string containing the event type JSON.
    Returns:
        dict: The extracted event type JSON.
    """
    def get_event_type_json(self, event_type_list_string: str) -> dict:
        return self.convert_string_to_json(event_type_list_string.split(' = ')[1].rstrip(';'))

    """
    Extracts the facility JSON from the provided string.
    Args:
        facility_list_string (str): The string containing the facility JSON.
    Returns:
        dict: The extracted facility JSON.
    """
    def get_facility_json(self, facility_list_string: str) -> dict:
        return self.convert_string_to_json(facility_list_string.split(' = ')[1].rstrip(';'))

    """
    Retrieves the facility name based on the provided facility ID.
    Args:
        facility_json (dict): The facility JSON data.
        facility_id (int): The ID of the facility to look up.
    Returns:
        str: The name of the facility, or None if not found.
    """
    @staticmethod
    def get_facility_name_by_id(facility_json, facility_id) -> str:
        for facility in facility_json:
            if facility['FacilityId'] == facility_id:
                return facility['ShortName']
        return ""

    """
    Retrieves the event name based on the provided event type ID.
    Args:
        event_type_json (dict): The event type JSON data.
        event_type_id (int): The ID of the event type to look up.
    Returns:
        str: The name of the event type, or None if not found.
    """
    @staticmethod
    def get_event_name_by_id(event_type_json, event_type_id) -> str:
        for event_type in event_type_json:
            if event_type['EventTypeId'] == event_type_id:
                return event_type['Name']
        return ""