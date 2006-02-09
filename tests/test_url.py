from unittest import TestCase
import unittest

from webhelpers.rails.url import *
from routes import *

class TestURLHelper(TestCase):
    def test_button_to_with_straight_url(self):
        self.assertEqual("<form method=\"post\" action=\"http://www.example.com\" class=\"button-to\"><div><input type=\"submit\" value=\"Hello\" /></div></form>", 
               button_to("Hello", "http://www.example.com"))

    def test_button_to_with_query(self):
        self.assertEqual("<form method=\"post\" action=\"http://www.example.com/q1=v1&amp;q2=v2\" class=\"button-to\"><div><input type=\"submit\" value=\"Hello\" /></div></form>", 
               button_to("Hello", "http://www.example.com/q1=v1&q2=v2"))
    
    def test_button_to_with_query_and_no_name(self):
        self.assertEqual("<form method=\"post\" action=\"http://www.example.com?q1=v1&amp;q2=v2\" class=\"button-to\"><div><input type=\"submit\" value=\"http://www.example.com?q1=v1&amp;q2=v2\" /></div></form>", 
               button_to(None, "http://www.example.com?q1=v1&q2=v2"))
    
    def test_button_to_with_javascript_confirm(self):
        self.assertEqual("<form method=\"post\" action=\"http://www.example.com\" class=\"button-to\"><div><input onclick=\"return confirm('Are you sure?');\" type=\"submit\" value=\"Hello\" /></div></form>",
               button_to("Hello", "http://www.example.com", confirm="Are you sure?"))
    
    def test_button_to_enabled_disabled(self):
        self.assertEqual("<form method=\"post\" action=\"http://www.example.com\" class=\"button-to\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
               button_to("Hello", "http://www.example.com", disabled=False))
        self.assertEqual("<form method=\"post\" action=\"http://www.example.com\" class=\"button-to\"><div><input disabled=\"disabled\" type=\"submit\" value=\"Hello\" /></div></form>",
               button_to("Hello", "http://www.example.com", disabled=True))

    def test_link_tag_with_straight_url(self):
        self.assertEqual("<a href=\"http://www.example.com\">Hello</a>", link_to("Hello", "http://www.example.com"))
    
    def test_link_tag_with_query(self):
        self.assertEqual("<a href=\"http://www.example.com?q1=v1&amp;q2=v2\">Hello</a>", 
               link_to("Hello", "http://www.example.com?q1=v1&q2=v2"))
    
    def test_link_tag_with_query_and_no_name(self):
        self.assertEqual("<a href=\"http://www.example.com?q1=v1&amp;q2=v2\">http://www.example.com?q1=v1&amp;q2=v2</a>", 
               link_to(None, "http://www.example.com?q1=v1&q2=v2"))
    
    def test_link_tag_with_custom_onclick(self):
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"alert('yay!')\">Hello</a>", 
               link_to("Hello", "http://www.example.com", onclick="alert('yay!')"))
    
    def test_link_tag_with_javascript_confirm(self):
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"return confirm('Are you sure?');\">Hello</a>",
               link_to("Hello", "http://www.example.com", confirm="Are you sure?"))
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"return confirm('You can\\'t possibly be sure, can you?');\">Hello</a>", 
               link_to("Hello", "http://www.example.com", confirm="You can't possibly be sure, can you?"))
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"return confirm('You can\\'t possibly be sure,\\n can you?');\">Hello</a>", 
               link_to("Hello", "http://www.example.com", confirm="You can't possibly be sure,\n can you?"))
    
    def test_link_tag_with_popup(self):
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"window.open(this.href);return false;\">Hello</a>",
               link_to("Hello", "http://www.example.com", popup=True))
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"window.open(this.href);return false;\">Hello</a>", 
               link_to("Hello", "http://www.example.com", popup='true'))
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"window.open(this.href,'window_name','width=300,height=300');return false;\">Hello</a>", 
               link_to("Hello", "http://www.example.com", popup=['window_name', 'width=300,height=300']))
    
    def test_link_tag_with_popup_and_javascript_confirm(self):
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"if (confirm('Fo\\' sho\\'?')) { window.open(this.href); };return false;\">Hello</a>",
               link_to("Hello", "http://www.example.com", popup=True, confirm="Fo' sho'?" ))
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"if (confirm('Are you serious?')) { window.open(this.href,'window_name','width=300,height=300'); };return false;\">Hello</a>",
               link_to("Hello", "http://www.example.com", popup=['window_name', 'width=300,height=300'],
                       confirm="Are you serious?"))
    
    def test_link_tag_using_post_javascript(self):
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"f = document.createElement('form'); document.body.appendChild(f); f.method = 'POST'; f.action = this.href; f.submit();return false;\">Hello</a>",
               link_to("Hello", "http://www.example.com", post=True))
    
    def test_link_tag_using_post_javascript_and_confirm(self):
        self.assertEqual("<a href=\"http://www.example.com\" onclick=\"if (confirm('Are you serious?')) { f = document.createElement('form'); document.body.appendChild(f); f.method = 'POST'; f.action = this.href; f.submit(); };return false;\">Hello</a>",
               link_to("Hello", "http://www.example.com", post=True, confirm="Are you serious?"))
    

if __name__ == '__main__':
    suite = [unittest.makeSuite(TestURLHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)