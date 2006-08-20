from unittest import TestCase
import unittest

from webhelpers.rails.number import *

class TestTextHelper(TestCase):
    def test_number_to_phone(self):
        self.assertEqual("123-555-1234", number_to_phone(1235551234))
        self.assertEqual("(123) 555-1234", number_to_phone(1235551234, area_code=True))
        self.assertEqual("123 555 1234", number_to_phone(1235551234, delimiter=" "))
        self.assertEqual("(123) 555-1234 x 555", number_to_phone(1235551234, area_code=True, extension=555))
        self.assertEqual("123-555-1234", number_to_phone(1235551234, extension="   "))

    def test_number_to_currency(self):
        self.assertEqual("$1,234,567,890.50", number_to_currency(1234567890.50))
        self.assertEqual("$1,234,567,890.51", number_to_currency(1234567890.506))
        self.assertEqual("$1,234,567,890", number_to_currency(1234567890.50, precision=0))
        self.assertEqual("$1,234,567,890.5", number_to_currency(1234567890.50, precision=1))
        self.assertEqual("&pound;1234567890,50", number_to_currency(1234567890.50, unit="&pound;", separator=",", delimiter=""))

    def test_number_to_percentage(self):
        self.assertEqual("100.000%", number_to_percentage(100))
        self.assertEqual("100%", number_to_percentage(100, precision=0))
        self.assertEqual("302.06%", number_to_percentage(302.0574, precision=2))

    def test_number_with_delimiter(self):
        self.assertEqual("12,345,678", number_with_delimiter(12345678))

    def test_number_to_human_size(self):
        self.assertEqual('0 Bytes', human_size(0))
        self.assertEqual('1 Byte', human_size(1))
        self.assertEqual('3 Bytes', human_size(3.14159265))
        self.assertEqual('123 Bytes', human_size(123.0))
        self.assertEqual('123 Bytes', human_size(123))
        self.assertEqual('1.2 KB', human_size(1234))
        self.assertEqual('12.1 KB', human_size(12345))
        self.assertEqual('1.2 MB', human_size(1234567))
        self.assertEqual('1.1 GB', human_size(1234567890))
        self.assertEqual('1.1 TB', human_size(1234567890123))
        self.assertEqual('', human_size('x'))
        self.assertEqual('', human_size(''))

    def test_number_with_precision(self):
        self.assertEqual("111.235", number_with_precision(111.2346))
