"""Date/Time Helpers"""
# Last synced with Rails copy at Revision 4674 on Aug 19th, 2006.

from datetime import datetime
import time

def distance_of_time_in_words(from_time, to_time=0, include_seconds=False):
    """
    Reports the approximate distance in time between two datetime objects or integers. 
    
    For example, if the distance is 47 minutes, it'll return
    "about 1 hour". See the source for the complete wording list.
    
    Integers are interpreted as seconds from now. So,
    ``distance_of_time_in_words(50)`` returns "less than a minute".
    
    Set ``include_seconds`` to True if you want more detailed approximations if distance < 1 minute
    """
    if isinstance(from_time, int):
        from_time = time.time()+from_time
    else:
        from_time = time.mktime(from_time.timetuple())
    if isinstance(to_time, int):
        to_time = time.time()+to_time
    else:
        to_time = time.mktime(to_time.timetuple())
    
    distance_in_minutes = int(round(abs(to_time-from_time)/60))
    distance_in_seconds = int(round(abs(to_time-from_time)))
    
    if distance_in_minutes <= 1:
        if include_seconds:
            for remainder in [5, 10, 20]:
                if distance_in_seconds < remainder:
                    return "less than %s seconds" % remainder
            if distance_in_seconds < 40:
                return "half a minute"
            elif distance_in_seconds < 60:
                return "less than a minute"
            else:
                return "1 minute"
        else:
            if distance_in_minutes == 0:
                return "less than a minute"
            else:
                return "1 minute"
    elif distance_in_minutes <= 45:
        return "%s minutes" % distance_in_minutes
    elif distance_in_minutes <= 90:
        return "about 1 hour"
    elif distance_in_minutes <= 1440:
        return "about %d hours" % (round(distance_in_minutes / 60.0))
    elif distance_in_minutes <= 2880:
        return "1 day"
    elif distance_in_minutes <= 43220:
        return "%d days" % (round(distance_in_minutes / 1440))
    elif distance_in_minutes <= 86400:
        return "about 1 month"
    elif distance_in_minutes <= 525960:
        return "%d months" % (round(distance_in_minutes / 43200))
    elif distance_in_minutes <= 1051920:
        return "about 1 year"
    else:
        return "over %d years" % (round(distance_in_minutes / 525600))

def time_ago_in_words(from_time, include_seconds=False):
    """
    Like distance_of_time_in_words, but where ``to_time`` is fixed to ``datetime.now()``.
    """
    return distance_of_time_in_words(from_time, datetime.now(), include_seconds)

def select_date(date=datetime.now(), **options):
    """
    Returns a set of html select-tags (one for year, month, day) pre-selected with the ``date``.
    """
    return select_year(date, options) + select_month(date, options) + select_day(date, options)

def select_datetime(datetime=datetime.now(), **options):
    """
    Returns a set of html select-tags (one for year, month, day, hour and minutes) pre-selected with the ``date``.
    """
    return select_year(datetime, options) + select_month(datetime, options) + select_day(datetime, options) + \
        select_hour(datetime, options) + select_minute(datetime, options)

def select_time(datetime=datetime.now(), **options):
    """Returns a set of html select-tags (one for hour and minute)
    
    ``include_seconds``
        Boolean to indicate if an additional select field for seconds should
        also be included.
    
    """
    seconds = ''
    if options.get('include_seconds'):
        del options['include_seconds']
        seconds = select_second(datetime, options)
    return select_hour(datetime, options) + select_minute(datetime, options) + seconds

def select_second(datetime, **options):
    """Returns a select tag with options for each of the seconds 0 through 59 with the
    current second selected.
    
    The 
    """
    pass

__all__ = ['distance_of_time_in_words', 'time_ago_in_words']
