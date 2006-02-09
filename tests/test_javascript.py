from unittest import TestCase
import unittest

from railshelpers.helpers.javascript import *

class TestJavascriptHelper(TestCase):
    def test_escape_javascript(self):
        self.assertEqual("""This \\"thing\\" is really\\n netos\\'""",
               escape_javascript("""This "thing" is really\n netos'"""))
    
    def test_link_to_funcion(self):
        self.assertEqual("""<a href="#" onclick="alert('Hello World!'); return false;">Greeting</a>""",
               link_to_function("Greeting", "alert('Hello World!')"))
    
    def test_link_to_function_with_html_args(self):
        self.assertEqual("""<a href="/home" onclick="alert('Hello World!'); return false;">Greeting</a>""",
               link_to_function("Greeting", "alert('Hello World!')", href="/home"))
    
    
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestJavascriptHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)