from datetime import datetime, timedelta

"""
Get the next occurrence of New Year's Day, Thanksgiving Day, and Christmas Day
Returns:
    datetime: The datetime object representing the next occurrence of the holiday.
"""
def get_the_next_new_years_day():
    month = 1
    day = 1
    return get_the_next_occurrence_of_a_given_holiday(month, day)

"""
Get the next occurrence of Thanksgiving Day (fourth Thursday in November)
Returns:
    datetime: The datetime object representing the next occurrence of Thanksgiving Day.
"""
def get_the_next_thanksgiving_day():
    year = datetime.now().year
    november_first = datetime(year, 11, 1)
    first_thursday_offset = (3 - november_first.weekday() + 7) % 7
    first_thursday = november_first + timedelta(days=first_thursday_offset)
    thanksgiving_day = first_thursday + timedelta(weeks=3)
    if thanksgiving_day < datetime.now():
        year += 1
        november_first = datetime(year, 11, 1)
        first_thursday_offset = (3 - november_first.weekday() + 7) % 7
        first_thursday = november_first + timedelta(days=first_thursday_offset)
        thanksgiving_day = first_thursday + timedelta(weeks=3)
    return thanksgiving_day

"""
Get the next occurrence of Christmas Day
Returns:
    datetime: The datetime object representing the next occurrence of Christmas Day.
"""
def get_the_next_christmas_day():
    month = 12
    day = 25
    return get_the_next_occurrence_of_a_given_holiday(month, day)

"""
Get the next occurrence of a given holiday based on month and day
Args:
    month (int): The month of the holiday.
    day (int): The day of the holiday.
Returns:
    datetime: The datetime object representing the next occurrence of the holiday.
"""
def get_the_next_occurrence_of_a_given_holiday(month: int, day: int):
    year = datetime.now().year
    if datetime.now().month == month and datetime.now().day > day:
        year += 1
    return datetime(year, month, day)

"""
Check if a given date is a holiday (New Year's Day, Thanksgiving Day, or Christmas Day)
Args:
    date (datetime): The date to check.
Returns:
    bool: True if the date is a holiday, False otherwise.
"""
def is_holiday(date: datetime) -> bool:
    holidays = [
        get_the_next_new_years_day(),
        get_the_next_thanksgiving_day(),
        get_the_next_christmas_day()
    ]
    for holiday in holidays:
        if date.month == holiday.month and date.day == holiday.day:
            return True
    return False