# -*- coding: utf-8 -*-
from unittest import TestCase
import unittest
from string24 import Template

from webhelpers.rails.text import *

class TestTextHelper(TestCase):
    
    def test_simple_format(self):
        self.assertEqual("<p></p>", simple_format(None))
        self.assertEqual("<p>crazy\n<br /> cross\n<br /> platform linebreaks</p>", simple_format("crazy\r\n cross\r platform linebreaks"))
        self.assertEqual("<p>A paragraph</p>\n\n<p>and another one!</p>", simple_format("A paragraph\n\nand another one!"))
        self.assertEqual("<p>A paragraph\n<br /> With a newline</p>", simple_format("A paragraph\n With a newline"))

    def test_auto_linking(self):
        
        raw_values = { 'email_raw': 'david@loudthinking.com',
                       'link_raw': 'http://www.rubyonrails.com',
                       'link2_raw': 'www.rubyonrails.com',
                       'link3_raw': 'http://manuals.ruby-on-rails.com/read/chapter.need_a-period/103#page281',
                       'link4_raw': 'http://foo.example.com/controller/action?parm=value&p2=v2#anchor123',
                       'link5_raw': 'http://www.rubyonrails.com.au',
                       'link6_raw': 'http://example.org/cgi-bin/some%20thing.cgi?foo=x&bar=37+x'
                     }
        
        result_values_templates = { 'email_result': '<a href="mailto:${email_raw}">${email_raw}</a>',
                                    'link_result': '<a href="${link_raw}">${link_raw}</a>',
                                    'link_result_with_options': '<a href="${link_raw}" target="_blank">${link_raw}</a>',
                                    'link2_result': '<a href="http://${link2_raw}">${link2_raw}</a>',
                                    'link3_result': '<a href="${link3_raw}">${link3_raw}</a>',
                                    'link4_result': '<a href="${link4_raw}">${link4_raw}</a>',
                                    'link5_result': '<a href="${link5_raw}">${link5_raw}</a>',
                                    'link6_result': '<a href="http://example.org/cgi-bin/some%20thing.cgi?foo=x&bar=37+x">http://example.org/cgi-bin/some%20thing.cgi?foo=x&bar=37+x</a>'
                                  }
                  
        result_values = {}
        for k, v in result_values_templates.iteritems():
            result_values[k] = Template(v).substitute(raw_values)
            
        self.assertEqual( 'hello %(email_result)s' %result_values, auto_link('hello %(email_raw)s' %raw_values, 'email_addresses'))
        self.assertEqual( 'Go to %(link_result)s' %result_values, auto_link('Go to %(link_raw)s' %raw_values, 'urls'))
        self.assertEqual( 'Go to %(link_raw)s' %raw_values, auto_link('Go to %(link_raw)s' %raw_values, 'email_addresses'))
        self.assertEqual( 'Go to %(link_result)s and say hello to %(email_result)s' %result_values, auto_link('Go to %(link_raw)s and say hello to %(email_raw)s' %raw_values))
        self.assertEqual( '<p>Link %(link_result)s</p>' %result_values, auto_link('<p>Link %(link_raw)s</p>' %raw_values))
        self.assertEqual( '<p>%(link_result)s Link</p>' %result_values, auto_link('<p>%(link_raw)s Link</p>' %raw_values))
        self.assertEqual( '<p>Link %(link_result_with_options)s</p>' %result_values, auto_link('<p>Link %(link_raw)s</p>' %raw_values, 'all', target='_blank'))
        self.assertEqual( 'Go to %(link_result)s.' %result_values, auto_link('Go to %(link_raw)s.' %raw_values))
        self.assertEqual( '<p>Go to %(link_result)s, then say hello to %(email_result)s.</p>' %result_values, auto_link('<p>Go to %(link_raw)s, then say hello to %(email_raw)s.</p>' %raw_values))
        
        self.assertEqual( 'Go to %(link2_result)s' %result_values, auto_link('Go to %(link2_raw)s' %raw_values, 'urls'))
        self.assertEqual( 'Go to %(link2_raw)s' %raw_values, auto_link('Go to %(link2_raw)s' %raw_values, 'email_addresses'))
        self.assertEqual( '<p>Link %(link2_result)s</p>' %result_values, auto_link('<p>Link %(link2_raw)s</p>' %raw_values))
        self.assertEqual( '<p>%(link2_result)s Link</p>' %result_values, auto_link('<p>%(link2_raw)s Link</p>' %raw_values))
        self.assertEqual( 'Go to %(link2_result)s.' %result_values, auto_link('Go to %(link2_raw)s.' %raw_values))
        self.assertEqual( '<p>Say hello to %(email_result)s, then go to %(link2_result)s.</p>' %result_values, auto_link('<p>Say hello to %(email_raw)s, then go to %(link2_raw)s.</p>' %raw_values))
        self.assertEqual( 'Go to %(link3_result)s' %result_values, auto_link('Go to %(link3_raw)s' %raw_values, 'urls'))
        self.assertEqual( 'Go to %(link3_raw)s' %raw_values, auto_link('Go to %(link3_raw)s' %raw_values, 'email_addresses'))
        self.assertEqual( '<p>Link %(link3_result)s</p>' %result_values, auto_link('<p>Link %(link3_raw)s</p>' %raw_values))
        self.assertEqual( '<p>%(link3_result)s Link</p>' %result_values, auto_link('<p>%(link3_raw)s Link</p>' %raw_values))
        self.assertEqual( 'Go to %(link3_result)s.' %result_values, auto_link('Go to %(link3_raw)s.' %raw_values))
        self.assertEqual( "<p>Go to %(link3_result)s. seriously, %(link3_result)s? i think I'll say hello to %(email_result)s. instead.</p>" %result_values, auto_link("<p>Go to %(link3_raw)s. seriously, %(link3_raw)s? i think I'll say hello to %(email_raw)s. instead.</p>" %raw_values))
        self.assertEqual( '<p>Link %(link4_result)s</p>' %result_values, auto_link('<p>Link %(link4_raw)s</p>' %raw_values))
        self.assertEqual( '<p>%(link4_result)s Link</p>' %result_values, auto_link('<p>%(link4_raw)s Link</p>' %raw_values))

        self.assertEqual( 'Go to %(link5_result)s' %result_values, auto_link('Go to %(link5_raw)s' %raw_values, 'urls'))
        self.assertEqual( 'Go to %(link5_raw)s' %raw_values, auto_link('Go to %(link5_raw)s' %raw_values, 'email_addresses'))
        self.assertEqual( '<p>Link %(link5_result)s</p>' %result_values, auto_link('<p>Link %(link5_raw)s</p>' %raw_values))
        self.assertEqual( '<p>%(link5_result)s Link</p>' %result_values, auto_link('<p>%(link5_raw)s Link</p>' %raw_values))
        self.assertEqual( 'Go to %(link5_result)s.' %result_values, auto_link('Go to %(link5_raw)s.' %raw_values))
        self.assertEqual( '<p>Say hello to %(email_result)s, then go to %(link5_result)s.</p>' %result_values, auto_link('<p>Say hello to %(email_raw)s, then go to %(link5_raw)s.</p>' %raw_values))
        self.assertEqual('%(link6_result)s' % result_values, auto_link('%(link6_raw)s' % raw_values))

    def test_excerpt(self):
        self.assertEqual("...lo my wo...",
                         excerpt("hello my world", "my", 3))
        self.assertEqual("...is a beautiful morn...",
                         excerpt("This is a beautiful morning", "beautiful", 5))
        self.assertEqual("This is a...",
                         excerpt("This is a beautiful morning", "this", 5))
        self.assertEqual("...iful morning",
                         excerpt("This is a beautiful morning", "morning", 5))
        self.assertEqual('',
                         excerpt("This is a beautiful morning", "day"))

    def test_excerpt_with_regex(self):
        self.assertEqual('...is a beautiful! mor...',
                         excerpt('This is a beautiful! morning', 'beautiful', 5))
        self.assertEqual('...is a beautiful? mor...',
                         excerpt('This is a beautiful? morning', 'beautiful', 5))

    def test_excerpt_with_utf8(self):
        self.assertEqual(u"...ﬃciency could not be ...",
                         excerpt(u"That's why eﬃciency could not be helped", 'could', 8))


    def test_highlighter(self):
        self.assertEqual("This is a <strong class=\"highlight\">beautiful</strong> morning",
                         highlight("This is a beautiful morning", "beautiful"))
        self.assertEqual(
            "This is a <strong class=\"highlight\">beautiful</strong> morning, but also a <strong class=\"highlight\">beautiful</strong> day",
            highlight("This is a beautiful morning, but also a beautiful day", "beautiful"))
        self.assertEqual("This is a <b>beautiful</b> morning, but also a <b>beautiful</b> day",
                         highlight("This is a beautiful morning, but also a beautiful day",
                                   "beautiful", r'<b>\1</b>'))
        self.assertEqual("This text is not changed because we supplied an empty phrase",
                         highlight("This text is not changed because we supplied an empty phrase",
                                   None))

    def test_highlighter_with_regex(self):
        self.assertEqual("This is a <strong class=\"highlight\">beautiful!</strong> morning",
                     highlight("This is a beautiful! morning", "beautiful!"))

        self.assertEqual("This is a <strong class=\"highlight\">beautiful! morning</strong>",
                     highlight("This is a beautiful! morning", "beautiful! morning"))

        self.assertEqual("This is a <strong class=\"highlight\">beautiful? morning</strong>",
                     highlight("This is a beautiful? morning", "beautiful? morning"))

    def test_strip_links(self):
        self.assertEqual("on my mind", strip_links("<a href='almost'>on my mind</a>"))
        self.assertEqual("on my mind", strip_links("<A href='almost'>on my mind</A>"))
        self.assertEqual("on my mind\nall day long",
                         strip_links("<a href='almost'>on my mind</a>\n<A href='almost'>all day long</A>"))

    def test_truncate(self):
        self.assertEqual("Hello World!", truncate("Hello World!", 12))
        self.assertEqual("Hello Wor...", truncate("Hello World!!", 12))

if __name__ == '__main__':
    suite = [unittest.makeSuite(TestTextHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
