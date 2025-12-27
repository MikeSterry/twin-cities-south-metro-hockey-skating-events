from datetime import datetime
from functools import total_ordering
from enums.Event_Type import EventType
from models.Arena import Arena
from models.Cost import Cost

@total_ordering
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
    start_time: datetime
    arena: Arena
    event_type: EventType
    end_time: datetime
    cost: Cost

    def __init__(self, event_type: EventType, arena: Arena, start_time: datetime, end_time: datetime, cost: Cost, notes: str = "") -> None:
        self.event_type = event_type
        self.arena = arena
        self.start_time = start_time
        self.end_time = end_time
        self.cost = cost
        self.notes = notes

    """
    Comparison methods to allow sorting events by multiple attributes.
    Args:
        other (Event): Another event to compare with.
    Returns:
        bool: True if this event is less than/equal to the other event based on defined
        attributes.
    """
    def __lt__(self, other) -> bool:
        if not isinstance(other, Event):
            return NotImplemented

        if self.start_time != other.start_time:
            return self.start_time < other.start_time

        if self.arena != other.arena:
            return self.arena < other.arena

        if self.event_type != other.event_type:
            return self.event_type.value < other.event_type.value

        if self.end_time != other.end_time:
            return self.start_time < other.start_time

        return self.cost.get_cost() < other.cost.get_cost()

    """
    Equality method to compare events by multiple attributes.
    Args:
        other (Event): Another event to compare with.
    Returns:
        bool: True if this event is equal to the other event based on defined attributes.
    """
    def __eq__(self, other) -> bool:
        if not isinstance(other, Event):
            return NotImplemented

        return (self.start_time == other.start_time and
                self.arena == other.arena and
                self.event_type == other.event_type and
                self.end_time == other.end_time and
                self.cost.get_cost() == other.cost.get_cost())

    """
    String representation of the Event object in JSON-like format.
    Returns:
        str: A string representation of the Event.
     """
    def __str__(self) -> str:
        return f'{{"event_type": "{self.event_type.name}", "arena": {{"name": "{self.arena.name}", "address": "{self.arena.address}", "notes": "{self.arena.notes}"}}, "start_time": "{self.start_time.strftime("%Y-%m-%d %H:%M")}", "end_time": "{self.end_time.strftime("%Y-%m-%d %H:%M")}", "cost": {{"adult_cost": {self.cost.adult_cost}, "child_cost": {self.cost.child_cost}}}}}'