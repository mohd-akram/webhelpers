from unittest import TestCase
import unittest
from string24 import Template

from railshelpers.helpers.text import *

class TestTextHelper(TestCase):
    
    def test_simple_format(self):
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
                     }
        
        result_values_templates = { 'email_result': '<a href="mailto:${email_raw}">${email_raw}</a>',
                                    'link_result': '<a href="${link_raw}">${link_raw}</a>',
                                    'link_result_with_options': '<a href="${link_raw}" target="_blank">${link_raw}</a>',
                                    'link2_result': '<a href="http://${link2_raw}">${link2_raw}</a>',
                                    'link3_result': '<a href="${link3_raw}">${link3_raw}</a>',
                                    'link4_result': '<a href="${link4_raw}">${link4_raw}</a>',
                                    'link5_result': '<a href="${link5_raw}">${link5_raw}</a>'
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

if __name__ == '__main__':
    suite = [unittest.makeSuite(TestTextHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
