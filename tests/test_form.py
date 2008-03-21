from util import WebHelpersTestCase
import unittest

from webhelpers.form import *

class TestFormHelper(WebHelpersTestCase):
    def test_array_options_for_select(self):
        self.assertEqual(
            "<option value=\"&lt;Denmark&gt;\">&lt;Denmark&gt;</option>\n<option value=\"USA\">USA</option>\n<option value=\"Sweden\">Sweden</option>",
            options_for_select([ "<Denmark>", "USA", "Sweden" ]))

    def test_array_options_for_select_with_selection(self):
        self.assertEqual(
            "<option value=\"Denmark\">Denmark</option>\n<option selected=\"selected\" value=\"&lt;USA&gt;\">&lt;USA&gt;</option>\n<option value=\"Sweden\">Sweden</option>",
            options_for_select([ "Denmark", "<USA>", "Sweden" ], "<USA>"))

    def test_array_options_for_select_with_selection_array(self):
        self.assertEqual(
            "<option value=\"Denmark\">Denmark</option>\n<option selected=\"selected\" value=\"&lt;USA&gt;\">&lt;USA&gt;</option>\n<option selected=\"selected\" value=\"Sweden\">Sweden</option>",
            options_for_select([ "Denmark", "<USA>", "Sweden" ], [ "<USA>", "Sweden" ]))

    def test_array_options_for_string_include_in_other_string_bug_fix(self):
        self.assertEqual(
            "<option value=\"ruby\">ruby</option>\n<option selected=\"selected\" value=\"rubyonrails\">rubyonrails</option>",
            options_for_select([ "ruby", "rubyonrails" ], "rubyonrails"))
        self.assertEqual(
            "<option selected=\"selected\" value=\"ruby\">ruby</option>\n<option value=\"rubyonrails\">rubyonrails</option>",
            options_for_select([ "ruby", "rubyonrails" ], "ruby"))
        self.assertEqual(
            '<option selected="selected" value="ruby">ruby</option>\n<option value="rubyonrails">rubyonrails</option>\n<option></option>',
            options_for_select([ "ruby", "rubyonrails", None ], "ruby"))

    def test_hash_options_for_select_with_dict(self):
        self.assertEqual(
            "<option value=\"&lt;Kroner&gt;\">&lt;DKR&gt;</option>\n<option value=\"Dollar\">$</option>",
            options_for_select({ "$": "Dollar", "<DKR>": "<Kroner>" }))
        self.assertEqual(
            "<option value=\"&lt;Kroner&gt;\">&lt;DKR&gt;</option>\n<option selected=\"selected\" value=\"Dollar\">$</option>",
            options_for_select({ "$": "Dollar", "<DKR>": "<Kroner>" }, "Dollar"))
        self.assertEqual(
            "<option selected=\"selected\" value=\"&lt;Kroner&gt;\">&lt;DKR&gt;</option>\n<option selected=\"selected\" value=\"Dollar\">$</option>",
            options_for_select({ "$": "Dollar", "<DKR>": "<Kroner>" }, [ "Dollar", "<Kroner>" ]))

    def test_options_for_select_from_objects(self):
        class Something(object):
            select_name = "something"
            select_value = "The Something"
        class SomethingElse(object):
            select_name = "somethingelse"
            select_value = "The Something Else"
        def make_elem(x):
            return x.select_name
        def make_elem_both(x):
            return x.select_name, x.select_value
        self.assertEqual('<option value="something">something</option>\n<option value="somethingelse">somethingelse</option>',
                         options_for_select([Something(), SomethingElse()], function=make_elem))
        self.assertEqual('<option selected="selected" value="something">something</option>\n<option value="somethingelse">somethingelse</option>',
                         options_for_select([Something(), SomethingElse()], selected='something', function=make_elem))
        self.assertEqual('<option value="The Something">something</option>\n<option value="The Something Else">somethingelse</option>',
                         options_for_select([Something(), SomethingElse()], function=make_elem_both))
        self.assertEqual('<option selected="selected" value="The Something">something</option>\n<option value="The Something Else">somethingelse</option>',
                         options_for_select([Something(), SomethingElse()], 'The Something', make_elem_both))

    def test_options_for_select_from_dicts(self):
        def make_elem_name(x):
            return x['select_name']
        def make_elem_both(x):
            return x['select_name'], x['select_value']

        something = dict(select_name="something",
                         select_value="The Something")
        somethingelse = dict(select_name="somethingelse",
                         select_value="The Something Else")
        self.assertEqual('<option value="something">something</option>\n<option value="somethingelse">somethingelse</option>',
                         options_for_select([something, somethingelse], function=make_elem_name))
        self.assertEqual('<option selected="selected" value="something">something</option>\n<option value="somethingelse">somethingelse</option>',
                         options_for_select([something, somethingelse], selected='something', function=make_elem_name))
        self.assertEqual('<option value="The Something">something</option>\n<option value="The Something Else">somethingelse</option>',
                         options_for_select([something, somethingelse], function=make_elem_both))
        self.assertEqual('<option selected="selected" value="The Something">something</option>\n<option value="The Something Else">somethingelse</option>',
                         options_for_select([something, somethingelse], 'The Something', make_elem_both))
    
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestFormHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
