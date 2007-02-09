from unittest import TestCase
import unittest

from webhelpers.rails.form_options import *

class TestFormOptionsHelper(TestCase):
    def test_array_options_for_select(self):
        self.assertEqual(
            "<option value=\"&lt;Denmark&gt;\">&lt;Denmark&gt;</option>\n<option value=\"USA\">USA</option>\n<option value=\"Sweden\">Sweden</option>",
            options_for_select([ "<Denmark>", "USA", "Sweden" ]))

    def test_array_options_for_select_with_selection(self):
        self.assertEqual(
            "<option value=\"Denmark\">Denmark</option>\n<option value=\"&lt;USA&gt;\" selected=\"selected\">&lt;USA&gt;</option>\n<option value=\"Sweden\">Sweden</option>",
            options_for_select([ "Denmark", "<USA>", "Sweden" ], "<USA>"))

    def test_array_options_for_select_with_selection_array(self):
      self.assertEqual(
        "<option value=\"Denmark\">Denmark</option>\n<option value=\"&lt;USA&gt;\" selected=\"selected\">&lt;USA&gt;</option>\n<option value=\"Sweden\" selected=\"selected\">Sweden</option>",
        options_for_select([ "Denmark", "<USA>", "Sweden" ], [ "<USA>", "Sweden" ]))

    def test_array_options_for_string_include_in_other_string_bug_fix(self):
        self.assertEqual(
            "<option value=\"ruby\">ruby</option>\n<option value=\"rubyonrails\" selected=\"selected\">rubyonrails</option>",
            options_for_select([ "ruby", "rubyonrails" ], "rubyonrails"))
        self.assertEqual(
            "<option value=\"ruby\" selected=\"selected\">ruby</option>\n<option value=\"rubyonrails\">rubyonrails</option>",
            options_for_select([ "ruby", "rubyonrails" ], "ruby"))
        self.assertEqual(
            '<option value="ruby" selected="selected">ruby</option>\n<option value="rubyonrails">rubyonrails</option>\n<option value=""></option>',
            options_for_select([ "ruby", "rubyonrails", None ], "ruby"))

    def test_hash_options_for_select_with_dict(self):
        self.assertEqual(
            "<option value=\"&lt;Kroner&gt;\">&lt;DKR&gt;</option>\n<option value=\"Dollar\">$</option>",
            options_for_select({ "$": "Dollar", "<DKR>": "<Kroner>" }))
        self.assertEqual(
            "<option value=\"&lt;Kroner&gt;\">&lt;DKR&gt;</option>\n<option value=\"Dollar\" selected=\"selected\">$</option>",
            options_for_select({ "$": "Dollar", "<DKR>": "<Kroner>" }, "Dollar"))
        self.assertEqual(
            "<option value=\"&lt;Kroner&gt;\" selected=\"selected\">&lt;DKR&gt;</option>\n<option value=\"Dollar\" selected=\"selected\">$</option>",
            options_for_select({ "$": "Dollar", "<DKR>": "<Kroner>" }, [ "Dollar", "<Kroner>" ]))

        """
    def test_ducktyped_options_for_select
    quack = Struct.new(:first, :last)
    self.assertEqual(
      "<option value=\"&lt;Kroner&gt;\">&lt;DKR&gt;</option>\n<option value=\"Dollar\">$</option>",
      options_for_select([quack.new("<DKR>", "<Kroner>"), quack.new("$", "Dollar")])
    )
    self.assertEqual(
      "<option value=\"&lt;Kroner&gt;\">&lt;DKR&gt;</option>\n<option value=\"Dollar\" selected=\"selected\">$</option>",
      options_for_select([quack.new("<DKR>", "<Kroner>"), quack.new("$", "Dollar")], "Dollar")
    )
    self.assertEqual(
      "<option value=\"&lt;Kroner&gt;\" selected=\"selected\">&lt;DKR&gt;</option>\n<option value=\"Dollar\" selected=\"selected\">$</option>",
      options_for_select([quack.new("<DKR>", "<Kroner>"), quack.new("$", "Dollar")], ["Dollar", "<Kroner>"])
    )
  end

  """
    
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestFormOptionsHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
