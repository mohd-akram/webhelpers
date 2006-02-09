from unittest import TestCase
import unittest

from railshelpers.helpers.tag import *

class TestTagHelper(TestCase):
    def test_tag(self):
        self.assertEqual("<p class=\"show\" />", tag("p", class_='show'))
    
    def test_tag_options(self):
        self.assertEqual("<p class=\"elsewhere\" />", tag("p", class_='elsewhere'))
    
    def test_tag_options_reject_none_option(self):
        self.assertEqual("<p />", tag("p", ignored=None))
    
    def test_tag_options_accept_blank_option(self):
        self.assertEqual("<p included=\"\" />", tag("p", included=''))
    
    def test_tag_options_converts_boolean_option(self):
        self.assertEqual('<p disabled="disabled" multiple="multiple" readonly="readonly" />',
               tag("p", disabled=True, multiple=True, readonly=True))
    
    def test_content_tag(self):
        self.assertEqual("<a href=\"create\">Create</a>", content_tag("a", "Create", href="create"))
    
        
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestTagHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)