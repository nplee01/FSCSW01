# Utilities

def to_date(date_str):
    # Convert ISO date string into date
    from time import strptime
    from datetime import date
    # ValueError Exception may be raised when input invalid 
    tm = strptime(date_str, '%Y-%m-%d')
    return date(tm.tm_year, tm.tm_mon, tm.tm_mday)
