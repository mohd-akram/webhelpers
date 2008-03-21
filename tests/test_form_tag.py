# -*- coding: utf-8 -*-
from util import WebHelpersTestCase
import unittest

from webhelpers.form_tag import *

class TestFormTagHelper(WebHelpersTestCase):
    def test_check_box(self):
        self.assertEqual(
            checkbox("admin"),
            u'<input id="admin" name="admin" type="checkbox" value="1" />',
        )

    def test_form(self):
        self.assertEqual(
            form(url="http://www.example.com"),
            u'<form action="http://www.example.com" method="POST">'
        )
        self.assertEqual(
            form(url="http://www.example.com", method='GET'),
            u'<form action="http://www.example.com" method="GET">'
        )
        self.assertEqual(
            form('/test/edit/1'),
            u'<form action="/test/edit/1" method="POST">'
        )

    def test_form_multipart(self):
        self.assertEqual(
            form(url='http://www.example.com', multipart=True),
            u'<form action="http://www.example.com" enctype="multipart/form-data" method="POST">'
        )
        
    def test_hidden_field(self):
        self.assertEqual(
            hidden("id", 3),
            u'<input id="id" name="id" type="hidden" value="3" />'
        )

    def test_hidden_field_alt(self):
        self.assertEqual(
            hidden("id", '3'),
            u'<input id="id" name="id" type="hidden" value="3" />'
        )

    def test_password_field(self):
        self.assertEqual(
            password(), 
            u'<input id="password" name="password" type="password" />'
        )

    def test_radio_button(self):
        self.assertEqual(
            radiobutton("people", "justin"),
            u'<input id="people_justin" name="people" type="radio" value="justin" />'
        )
        
        self.assertEqual(
            radiobutton("num_people", 5),
            u'<input id="num_people_5" name="num_people" type="radio" value="5" />'
        )

        self.assertEqual(
            radiobutton("num_people", 5),
            u'<input id="num_people_5" name="num_people" type="radio" value="5" />'
        )
        
        self.assertEqual(
            radiobutton("gender", "m") + radiobutton("gender", "f"),
            u'<input id="gender_m" name="gender" type="radio" value="m" /><input id="gender_f" name="gender" type="radio" value="f" />'
        )
        
        self.assertEqual(
            radiobutton("opinion", "-1") + radiobutton("opinion", "1"),
            u'<input id="opinion_-1" name="opinion" type="radio" value="-1" /><input id="opinion_1" name="opinion" type="radio" value="1" />'
        )

        self.assertEqual(
            radiobutton("num_people", 5, checked=True),
            u'<input checked="checked" id="num_people_5" name="num_people" type="radio" value="5" />'
        )

    def test_submit(self):
        self.assertEqual(
            u'<input name="commit" type="submit" value="Save changes" />',
            submit()
        )

    def test_text_area(self):
        self.assertEqual(
            textarea("aa", ""),
            u'<textarea id="aa" name="aa"></textarea>'
        )
        self.assertEqual(
            textarea("aa", None),
            u'<textarea id="aa" name="aa"></textarea>'
        )
        self.assertEqual(
            textarea("aa", "Hello!"),
            u'<textarea id="aa" name="aa">Hello!</textarea>'
        )

    def test_text_area_size_string(self):
        self.assertEqual(
            textarea("body", "hello world", size = "20x40"),
            u'<textarea cols="20" id="body" name="body" rows="40">hello world</textarea>'
        )

    def test_text_field(self):
        self.assertEqual(
            text("title", ""),
            u'<input id="title" name="title" type="text" value="" />'
        )
        self.assertEqual(
            text("title", None),
            u'<input id="title" name="title" type="text" />'
        )
        self.assertEqual(
            text("title", "Hello!"),
            u'<input id="title" name="title" type="text" value="Hello!" />'
        )

    def test_text_field_class_string(self):
        self.assertEqual(
            text( "title", "Hello!", class_= "admin"),
            u'<input class="admin" id="title" name="title" type="text" value="Hello!" />'
        )

    def test_boolean_options(self):
        self.assertEqual(     
            checkbox("admin", 1, True, disabled = True, readonly="yes"),
            u'<input checked="checked" disabled="disabled" id="admin" name="admin" readonly="readonly" type="checkbox" value="1" />'
        )
        self.assertEqual(
            checkbox("admin", 1, True, disabled = False, readonly = None),
            u'<input checked="checked" id="admin" name="admin" type="checkbox" value="1" />'
        )

    
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestFormTagHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
