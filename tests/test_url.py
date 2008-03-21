from util import WebHelpersTestCase
import unittest

from webhelpers.urls import *
from webhelpers.html import HTML
from routes import *

class TestURLHelper(WebHelpersTestCase):
    def test_button_to_with_straight_url(self):
        self.assertEqual(u"<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>", 
               button_to("Hello", "http://www.example.com"))

    def test_button_to_with_query(self):
        self.assertEqual(u"<form action=\"http://www.example.com/q1=v1&amp;q2=v2\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>", 
               button_to("Hello", "http://www.example.com/q1=v1&q2=v2"))

    def test_button_to_with_escaped_query(self):
        self.assertEqual(u"<form action=\"http://www.example.com/q1=v1&amp;q2=v2\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
                         button_to("Hello", "http://www.example.com/q1=v1&q2=v2"))
    
    def test_button_to_with_query_and_no_name(self):
        self.assertEqual(u"<form action=\"http://www.example.com?q1=v1&amp;q2=v2\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"http://www.example.com?q1=v1&amp;q2=v2\" /></div></form>", 
               button_to(None, "http://www.example.com?q1=v1&q2=v2"))
    
    def test_button_to_enabled_disabled(self):
        self.assertEqual(u"<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
               button_to("Hello", "http://www.example.com", disabled=False))
        self.assertEqual(u"<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input disabled=\"disabled\" type=\"submit\" value=\"Hello\" /></div></form>",
               button_to("Hello", "http://www.example.com", disabled=True))
    
    def test_button_to_with_method_delete(self):
        self.assertEqual(u"<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input id=\"_method\" name=\"_method\" type=\"hidden\" value=\"DELETE\" /><input type=\"submit\" value=\"Hello\" /></div></form>", 
            button_to("Hello", "http://www.example.com", method='DELETE'))
        self.assertEqual(u"<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input id=\"_method\" name=\"_method\" type=\"hidden\" value=\"delete\" /><input type=\"submit\" value=\"Hello\" /></div></form>", 
            button_to("Hello", "http://www.example.com", method='delete'))

    def test_button_to_with_method_get(self):
        self.assertEqual(u"<form action=\"http://www.example.com\" class=\"button-to\" method=\"get\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
            button_to("Hello", "http://www.example.com", method='get'))
        self.assertEqual(u"<form action=\"http://www.example.com\" class=\"button-to\" method=\"GET\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
            button_to("Hello", "http://www.example.com", method='GET'))

    def test_button_to_with_img(self):
        self.assertEqual(u'<form action="/content/edit/3" class="button-to" method="POST"><div><input alt="Edit" src="/images/icon_delete.gif" type="image" value="Edit" /></div></form>',
                         button_to("Edit", url_for(action='edit', id=3), type='image', src='icon_delete.gif'))
        self.assertEqual(u'<form action="/content/submit/3" class="button-to" method="POST"><div><input alt="Complete the form" src="/images/submit.png" type="image" value="Submit" /></div></form>',
                         button_to("Submit", url_for(action='submit', id=3), type='image', src='submit', alt='Complete the form'))

    def test_link_tag_with_straight_url(self):
        self.assertEqual(u"<a href=\"http://www.example.com\">Hello</a>", link_to("Hello", "http://www.example.com"))
    
    def test_link_tag_with_query(self):
        self.assertEqual(u"<a href=\"http://www.example.com?q1=v1&amp;q2=v2\">Hello</a>", 
               link_to("Hello", "http://www.example.com?q1=v1&q2=v2"))
    
    def test_link_tag_with_query_and_no_name(self):
        self.assertEqual(u"<a href=\"http://www.example.com?q1=v1&amp;q2=v2\">http://www.example.com?q1=v1&amp;q2=v2</a>", 
               link_to(None, HTML.literal("http://www.example.com?q1=v1&amp;q2=v2")))
    
    def test_link_tag_with_custom_onclick(self):
        self.assertEqual(u"<a href=\"http://www.example.com\" onclick=\"alert('yay!')\">Hello</a>", 
               link_to("Hello", "http://www.example.com", onclick="alert('yay!')"))
    
    def test_mail_to(self):
        self.assertEqual(u'<a href="mailto:justin@example.com">justin@example.com</a>', mail_to("justin@example.com"))
        self.assertEqual(u'<a href="mailto:justin@example.com">Justin Example</a>', mail_to("justin@example.com", "Justin Example"))
        self.assertEqual(u'<a class="admin" href="mailto:justin@example.com">Justin Example</a>',
                         mail_to("justin@example.com", "Justin Example", class_="admin"))

    def test_mail_to_with_javascript(self):
        self.assertEqual(u"<script type=\"text/javascript\">\n//<![CDATA[\neval(unescape('%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%27%3c%61%20%68%72%65%66%3d%22%6d%61%69%6c%74%6f%3a%6d%65%40%64%6f%6d%61%69%6e%2e%63%6f%6d%22%3e%4d%79%20%65%6d%61%69%6c%3c%2f%61%3e%27%29%3b'))\n//]]>\n</script>", mail_to("me@domain.com", "My email", encode = "javascript"))

    def test_mail_to_with_options(self):
        self.assertEqual(u'<a href="mailto:me@example.com?cc=ccaddress%40example.com&amp;body=This%20is%20the%20body%20of%20the%20message.&amp;subject=This%20is%20an%20example%20email&amp;bcc=bccaddress%40example.com">My email</a>',
            mail_to("me@example.com", "My email", cc="ccaddress@example.com",
                    bcc="bccaddress@example.com", subject="This is an example email",
                    body="This is the body of the message."))

    def test_mail_to_with_img(self):
        self.assertEqual(u'<a href="mailto:feedback@example.com"><img src="/feedback.png" /></a>',
                        mail_to('feedback@example.com', HTML.literal('<img src="/feedback.png" />')))

    def test_mail_to_with_hex(self):
        self.assertEqual(u"<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">My email</a>",
                         mail_to("me@domain.com", "My email", encode = "hex"))
        self.assertEqual(u"<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">&#109;&#101;&#64;&#100;&#111;&#109;&#97;&#105;&#110;&#46;&#99;&#111;&#109;</a>",
                         mail_to("me@domain.com", None, encode = "hex"))

    def test_mail_to_with_replace_options(self):
        self.assertEqual(u'<a href="mailto:wolfgang@stufenlos.net">wolfgang(at)stufenlos(dot)net</a>',
                        mail_to("wolfgang@stufenlos.net", None, replace_at="(at)", replace_dot="(dot)"))
        self.assertEqual(u"<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">&#109;&#101;&#40;&#97;&#116;&#41;&#100;&#111;&#109;&#97;&#105;&#110;&#46;&#99;&#111;&#109;</a>",
                         mail_to("me@domain.com", None, encode = "hex", replace_at = "(at)"))
        self.assertEqual(u"<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">My email</a>",
                         mail_to("me@domain.com", "My email", encode = "hex", replace_at = "(at)"))
        self.assertEqual(u"<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">&#109;&#101;&#40;&#97;&#116;&#41;&#100;&#111;&#109;&#97;&#105;&#110;&#40;&#100;&#111;&#116;&#41;&#99;&#111;&#109;</a>",
                         mail_to("me@domain.com", None, encode = "hex", replace_at = "(at)", replace_dot = "(dot)"))
        self.assertEqual(u"<script type=\"text/javascript\">\n//<![CDATA[\neval(unescape('%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%27%3c%61%20%68%72%65%66%3d%22%6d%61%69%6c%74%6f%3a%6d%65%40%64%6f%6d%61%69%6e%2e%63%6f%6d%22%3e%4d%79%20%65%6d%61%69%6c%3c%2f%61%3e%27%29%3b'))\n//]]>\n</script>",
                         mail_to("me@domain.com", "My email", encode = "javascript", replace_at = "(at)", replace_dot = "(dot)"))

if __name__ == '__main__':
    suite = [unittest.makeSuite(TestURLHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
