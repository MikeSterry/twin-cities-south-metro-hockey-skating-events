class Cost:
    """
    Class to represent the cost associated with an event.
    Attributes:
        cost (float): The monetary cost of the event.
        notes (str): Additional notes regarding the cost.
    """
    def __init__(self, cost: float = 0.0, notes: str = ""):
        self.cost = cost
        self.notes = notes

    """
    Set the cost of the event.
    Args:
        cost (float): The monetary cost to set for the event.
    """
    def set_cost(self, cost: float) -> None:
        self.cost = cost

    """
    Set additional notes regarding the cost.
    Args:
        notes (str): The notes to set regarding the cost.
    """
    def add_notes(self, notes: str) -> None:
        self.notes = notes

    """
    Get the cost of the event.
    Returns:
        float: The monetary cost of the event.
    """
    def get_cost(self) -> float:
        return self.cost

    """
    Get additional notes regarding the cost.
    Returns:
        str: The notes regarding the cost.
    """
    def get_notes(self) -> str:
        return self.notes