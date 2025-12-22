class Address:
    """
    A class representing a physical address with street, city, state, and zip code.
    """
    def __init__(self, street: str, city: str, state: str, zip_code: str):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    """
    Returns the full address as a formatted string.
    """
    def get_address_string(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

    """
    Returns the city name from the address.
    """
    def get_city_name(self) -> str:
        return self.city

    def __repr__(self):
        return (f"Address(street='{self.street}', city='{self.city}', "
                f"state='{self.state}', zip_code='{self.zip_code}'')")