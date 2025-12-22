from enum import Enum

class EventType(Enum):
    """
    Enumeration for different types of skating events.
    OPEN_SKATE: Represents open skate sessions.
    STICK_AND_PUCK: Represents stick and puck sessions, or sometimes referred to as Developmental Hockey.
    """
    OPEN_SKATE = "Open Skate"
    STICK_AND_PUCK = "Stick and Puck"