from unittest import TestCase
import unittest

from webhelpers.rails.form_tag import *

class TestFormTagHelper(TestCase):
    def test_check_box(self):
        self.assertEqual(
            check_box("admin"),
            '<input id="admin" name="admin" type="checkbox" value="1" />',
        )

    def test_form(self):
        self.assertEqual(
            form(url="http://www.example.com"),
            '<form action="http://www.example.com" method="post">'
        )

    def test_form_multipart(self):
        self.assertEqual(
            form(url='http://www.example.com', multipart=True),
            '<form action="http://www.example.com" enctype="multipart/form-data" method="post">'
        )
            
    def test_hidden_field(self):
        self.assertEqual(
            hidden_field("id", 3),
            '<input id="id" name="id" type="hidden" value="3" />'
        )

    def test_hidden_field_alt(self):
        self.assertEqual(
            hidden_field("id", '3'),
            '<input id="id" name="id" type="hidden" value="3" />'
        )

    def test_password_field(self):
        self.assertEqual(
            password_field(), 
            '<input id="password" name="password" type="password" />'
        )

    def test_radio_button(self):
        self.assertEqual(
            radio_button("people", "justin"),
            '<input id="people" name="people" type="radio" value="justin" />'
        )

    def test_select(self):
        self.assertEqual(
            select("people", "<option>justin</option>"),
            '<select id="people" name="people"><option>justin</option></select>'
        )

    def test_text_area_size_string(self):
        self.assertEqual(
            text_area("body", "hello world", size = "20x40"),
            '<textarea cols="20" id="body" name="body" rows="40">hello world</textarea>'
        )

    def test_text_field(self):
        self.assertEqual(
            text_field("title", "Hello!"),
            '<input id="title" name="title" type="text" value="Hello!" />'
        )

    def test_text_field_class_string(self):
        self.assertEqual(
            text_field( "title", "Hello!", class_= "admin"),
            '<input class="admin" id="title" name="title" type="text" value="Hello!" />'
        )

    def test_boolean_options(self):
        self.assertEqual(     
            check_box("admin", 1, True, disabled = True, readonly="yes"),
            '<input checked="checked" disabled="disabled" id="admin" name="admin" readonly="readonly" type="checkbox" value="1" />'
        )
        self.assertEqual(
            check_box("admin", 1, True, disabled = False, readonly = None),
            '<input checked="checked" id="admin" name="admin" type="checkbox" value="1" />'
        )
        self.assertEqual(
            select("people", "<option>justin</option>", multiple = True),
            '<select id="people" multiple="multiple" name="people"><option>justin</option></select>'
        )

        self.assertEqual(
            select("people", "<option>justin</option>", multiple = None),
            '<select id="people" name="people"><option>justin</option></select>'
        )

    
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestFormTagHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
