"""
Date/Time Helpers
"""

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
    else:
        return "%s days" % (distance_in_minutes / 1440)

def time_ago_in_words(from_time, include_seconds=False):
    """
    Like distance_of_time_in_words, but where ``to_time`` is fixed to ``datetime.now()``.
    """
    return distance_of_time_in_words(from_time, datetime.now(), include_seconds)

distance_of_time_in_words_to_now = time_ago_in_words


__all__ = ['distance_of_time_in_words', 'time_ago_in_words', 'distance_of_time_in_words_to_now']
