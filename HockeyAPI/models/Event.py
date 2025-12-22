from datetime import datetime

from enums.Event_Type import EventType
from models.Arena import Arena
from models.Cost import Cost

class Event:
    """
    Represents an event at an arena.
    Attributes:
        event_type (EventType): The type of the event.
        arena (Arena): The arena where the event takes place.
        start_time (datetime): The start time of the event.
        end_time (datetime): The end time of the event.
        cost (Cost): The cost associated with the event.
        notes (str): Additional notes about the event.
    """
    def __init__(self, event_type: EventType, arena: Arena, start_time: datetime, end_time: datetime, cost: Cost, notes: str = "") -> None:
        self.event_type = event_type
        self.arena = arena
        self.start_time = start_time
        self.end_time = end_time
        self.cost = cost
        self.notes = notes

    def __str__(self) -> str:
        return f'{{"event_type": "{self.event_type.name}", "arena": {{"name": "{self.arena.name}", "address": "{self.arena.address}", "notes": "{self.arena.notes}"}}, "start_time": "{self.start_time.strftime("%Y-%m-%d %H:%M")}", "end_time": "{self.end_time.strftime("%Y-%m-%d %H:%M")}", "cost": {{"adult_cost": {self.cost.adult_cost}, "child_cost": {self.cost.child_cost}}}}}'