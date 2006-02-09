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

        # additional tests
        # exactly 24 hrs should be about 24 hrs - to be the same as Rails (it should be 1 day)
        self.assertEqual("about 24 hours", distance_of_time_in_words(from_time, datetime(2004, 3, 7, 21, 41, 18)))
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
        # exactly 24 hrs should be about 24 hrs - to be the same as Rails (it should be 1 day)
        self.assertEqual("about 24 hours", distance_of_time_in_words(86400))
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