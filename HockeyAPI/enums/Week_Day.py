from enum import Enum

class WeekDay(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def get_weekday(weekday_name: str) -> 'WeekDay':
        """
        Returns the WeekDay enum member corresponding to the given weekday name.

        Args:
            weekday_name (str): The name of the weekday (e.g., "Monday", "Tuesday").

        Returns:
            WeekDay: The corresponding WeekDay enum member.

        Raises:
            ValueError: If the provided weekday name does not match any enum member.
        """
        try:
            return WeekDay[weekday_name.upper()]
        except KeyError:
            raise ValueError(f"{weekday_name} is not a valid weekday name.")