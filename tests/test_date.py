from unittest import TestCase
import unittest
from datetime import datetime
from datetime import timedelta
import time

from webhelpers.rails.date import *

class TestDateHelper(TestCase):
    
    def test_distance_of_time_in_words(self):
        from_time = datetime(2004, 3, 6, 21, 41, 18)

        # ported from Rails tests
        self.assertEqual("less than a minute", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 41, 25)))
        self.assertEqual("5 minutes", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 46, 25)))
        self.assertEqual("about 1 hour", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 22, 47, 25)))
        self.assertEqual("about 3 hours", distance_of_time_in_words(from_time, datetime(2004, 3, 7, 0, 41)))
        self.assertEqual("about 4 hours", distance_of_time_in_words(from_time, datetime(2004, 3, 7, 1, 20)))
        self.assertEqual("2 days", distance_of_time_in_words(from_time, datetime(2004, 3, 9, 15, 40)))
        
        # test greater date separation
        self.assertEqual("29 days", distance_of_time_in_words(from_time, datetime(2004, 4, 5, 12, 41, 18)))
        self.assertEqual("about 1 month", distance_of_time_in_words(from_time, datetime(2004, 4, 6, 21, 41, 18)))
        self.assertEqual("about 1 month", distance_of_time_in_words(from_time, datetime(2004, 4, 7, 21, 41, 18)))
        self.assertEqual("2 months", distance_of_time_in_words(from_time, datetime(2004, 5, 6, 21, 41, 18)))
        self.assertEqual("11 months", distance_of_time_in_words(from_time, datetime(2005, 2, 6, 21, 41, 18)))
        self.assertEqual("about 1 year", distance_of_time_in_words(from_time, datetime(2005, 4, 6, 21, 41, 18)))
        self.assertEqual("about 1 year", distance_of_time_in_words(from_time, datetime(2005, 4, 12, 21, 41, 18)))
        self.assertEqual("over 2 years", distance_of_time_in_words(from_time, datetime(2006, 4, 6, 21, 41, 18)))
        
        # include seconds 
        self.assertEqual("less than a minute", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 41, 19), False))
        self.assertEqual("less than 5 seconds", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 41, 19), True))
        self.assertEqual("less than 10 seconds", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 41, 27), True))
        self.assertEqual("less than 20 seconds", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 41, 37), True))
        self.assertEqual("half a minute", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 41, 48), True))
        self.assertEqual("less than a minute", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 42, 17), True))

        self.assertEqual("1 minute", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 42, 18), True))
        self.assertEqual("1 minute", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 42, 28), True))
        self.assertEqual("2 minutes", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 42, 48), True))
        
        # test to < from
        self.assertEqual("about 4 hours", distance_of_time_in_words(datetime(2004, 3, 7, 1, 20), from_time))
        self.assertEqual("less than 20 seconds", distance_of_time_in_words(datetime(2004, 3, 6, 21, 41, 37), from_time, True))

        # test with integers
        self.assertEqual("less than a minute", distance_of_time_in_words(29))
        self.assertEqual("about 1 hour", distance_of_time_in_words(60*60))

        # more cumbersome test with integers
        self.assertEqual("less than a minute", distance_of_time_in_words(0, 29))
        self.assertEqual("about 1 hour", distance_of_time_in_words(60*60, 0))
        
        # additional tests
        # exactly 24 hrs
        self.assertEqual("1 day", distance_of_time_in_words(from_time, datetime(2004, 3, 7, 21, 51, 18)))
        # test > 30, but < 60 s, i.e. closer to a minute if rounded
        self.assertEqual("1 minute", distance_of_time_in_words(from_time, datetime(2004, 3, 6, 21, 41, 50)))
        
        # test from, to as int
        self.assertEqual("less than a minute", distance_of_time_in_words(18, 25))
        self.assertEqual("1 minute", distance_of_time_in_words(1, 50))
        self.assertEqual("5 minutes", distance_of_time_in_words(10, 310))
        self.assertEqual("about 1 hour", distance_of_time_in_words(100, 100+66*60))
        self.assertEqual("about 3 hours", distance_of_time_in_words(11160))
        self.assertEqual("about 4 hours", distance_of_time_in_words(14399))
        self.assertEqual("2 days", distance_of_time_in_words(180000))
        # exactly 24 hrs
        self.assertEqual("1 day", distance_of_time_in_words(86400))
        self.assertEqual("1 day", distance_of_time_in_words(87000))

    def test_time_ago_in_words(self):
        self.assertEqual("less than a minute", time_ago_in_words(25))
        self.assertEqual("5 minutes", time_ago_in_words(320))
        self.assertEqual("about 1 hour", time_ago_in_words(68*60))
        # and now for something completely different
        self.assertEqual("about 3 hours", time_ago_in_words(datetime.now() - timedelta(hours=3, minutes=13)))
        self.assertEqual("about 4 hours", time_ago_in_words(datetime.now() + timedelta(hours=3, minutes=56)))
        self.assertEqual("2 days", time_ago_in_words(datetime.now() - timedelta(days=2, hours=3, minutes=13)))
        
        
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestDateHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
