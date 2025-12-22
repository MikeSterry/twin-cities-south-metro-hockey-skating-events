from models.Address import Address


class Arena:
    """
    A class representing a sports arena with attributes for name, address, and notes.
    Attributes:
        name (str): The name of the arena.
        address (str): The physical address of the arena.
        notes (str): Additional notes about the arena.
    """
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

    def __str__(self):
        return f"Arena(Name: {self.name}, Address: {self.get_address()}, Notes: {self.notes})"