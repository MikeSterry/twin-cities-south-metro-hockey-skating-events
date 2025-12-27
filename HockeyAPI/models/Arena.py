from functools import total_ordering
from models.Address import Address


@total_ordering
class Arena:
    """
    A class representing a sports arena with attributes for name, address, and notes.
    Attributes:
        name (str): The name of the arena.
        address (str): The physical address of the arena.
        notes (str): Additional notes about the arena.
    """
    name: str

    def __init__(self, name: str, address: Address, notes: str = ""):
        self.name = name
        self.address = address
        self.notes = notes

    """
    Set the notes for the arena.
    Args:
        notes (str): The notes to set for the arena.
    """
    def set_notes(self, notes: str):
        self.notes = notes

    """
    Get the address of the arena as a string.
    Returns:
        str: The address of the arena.
    """
    def get_address(self) -> str:
        return self.address.get_address_string()

    """
    Get the city name from the arena's address.
    Returns:
        str: The city name of the arena.
    """
    def get_city_name(self) -> str:
        return self.address.get_city_name()

    """
    Comparison methods to allow sorting arenas by name.
    Args:
        other (Arena): Another arena to compare with.
    Returns:
        bool: True if this arena's name is less than/equal to the other arena's name.
    """
    def __lt__(self, other) -> bool:
        if not isinstance(other, Arena):
            return NotImplemented

        return self.name < other.name

    """
    Equality method to compare arenas by name.
    Args:
        other (Arena): Another arena to compare with.
    Returns:
        bool: True if the arena names are equal.
    """
    def __eq__(self, other) -> bool:
        if not isinstance(other, Arena):
            return NotImplemented
        return self.name == other.name

    """
    Check if an instance is of type Arena.
    Args:
        instance: The instance to check.
    Returns:
        bool: True if the instance is an Arena, False otherwise.
    """
    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, Arena)

    """
    String representation of the Arena object.
    Returns:
        str: A string describing the arena.
    """
    def __str__(self) -> str:
        return f"Arena(Name: {self.name}, Address: {self.get_address()}, Notes: {self.notes})"

    """
    Hash method to allow using Arena instances in sets and as dictionary keys.
    Returns:
        int: The hash value of the Arena instance.
    """
    def __hash__(self) -> int:
        return hash((self.name, self.address.get_address_string(), self.notes))