from enum import Enum

class EventType(Enum):
    """
    Enumeration for different types of skating events.
    OPEN_SKATE: Represents open skate sessions.
    STICK_AND_PUCK: Represents stick and puck sessions, or sometimes referred to as Developmental Hockey.
    """
    OPEN_SKATE = "Open Skate"
    STICK_AND_PUCK = "Stick and Puck"

    """
    Returns the priority of the event type for sorting purposes.
    Lower values indicate higher priority.
    OPEN_SKATE has higher priority than STICK_AND_PUCK.
    """
    @property
    def priotity(self) -> int:
        priorities = {
            EventType.OPEN_SKATE: 1,
            EventType.STICK_AND_PUCK: 2
        }
        return priorities[self]