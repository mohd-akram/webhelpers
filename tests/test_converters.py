# -*- coding: utf-8 -*-
from util import WebHelpersTestCase
import unittest

from webhelpers.html import HTML, literal
from webhelpers.html.converters import markdown, textilize

class TestConvertersHelper(WebHelpersTestCase):
    
    def test_textilize(self):
        self.assertEqual('<h1>This is a test of textile</h1>\n\n<p>Paragraph</p>\n\n<p>Another paragraph</p>\n\n<ul>\n<li>Bullets</li>\n</ul>',
                         textilize("h1. This is a test of textile\n\nParagraph\n\nAnother paragraph\n\n* Bullets"))

    def test_markdown(self):
        markdown_text = """
Introduction
------------

Markdown is a text-to-HTML conversion tool for web writers.

Acknowledgements <a id="acknowledgements" />
----------------

[Michel Fortin][] has ported to Markdown to PHP.
        """
        self.assertEqual('\n\n<h2>Introduction</h2>\n<p>Markdown is a text-to-HTML conversion tool for web writers.\n</p>\n\n<h2>Acknowledgements <a id="acknowledgements" /></h2>\n<p>[Michel Fortin][] has ported to Markdown to PHP.\n</p>\n\n\n',
                         markdown(markdown_text))


if __name__ == '__main__':
    suite = map(unittest.makeSuite, [
        TestConvertersHelper,
        ])
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
