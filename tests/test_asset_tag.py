from unittest import TestCase
import unittest

from webhelpers.rails.asset_tag import *

class TestAssetTagHelper(TestCase):
    def test_image_tag(self):
        self.assertEqual('<img alt="Xml" src="/images/xml.png" />',
                         image_tag('xml'))
        self.assertEqual('<img alt="rss syndication" src="/images/rss.png" />',
                        image_tag('rss', alt='rss syndication'))
        self.assertEqual('<img alt="Gold" height="70" src="/images/gold.png" width="45" />',
                         image_tag('gold', size='45x70'))
        self.assertEqual('<img alt="Symbolize" height="70" src="/images/symbolize.png" width="45" />',
                         image_tag('symbolize', size='45x70'))
        self.assertEqual('<img alt="Pylons-Tower-Dark1" src="http://pylons.tgtg.org/powered/_img/pylons-tower-dark1.png" />',
                         image_tag('http://pylons.tgtg.org/powered/_img/pylons-tower-dark1.png'))

    def test_javascript_include_tag(self):
        self.assertEqual("""<script src="/javascripts/prototype.js" type="text/javascript"></script>\n<script src="/javascripts/scriptaculous.js" type="text/javascript"></script>""",
                         javascript_include_tag(builtins=True))
        self.assertEqual("""<script src="/javascripts/prototype.js" type="text/javascript"></script>\n<script src="/other-javascripts/util.js" type="text/javascript"></script>""",
                         javascript_include_tag('prototype', '/other-javascripts/util.js'))
        self.assertEqual("""<script src="/javascripts/prototype.js" type="text/javascript"></script>\n<script src="/javascripts/scriptaculous.js" type="text/javascript"></script>\n<script src="/javascripts/app.js" type="text/javascript"></script>\n<script src="/test/test.1.js" type="text/javascript"></script>""",
                         javascript_include_tag('app', '/test/test.1.js', builtins=True))

    def test_stylesheet_link_tag(self):
        self.assertEqual('<link href="/stylesheets/style.css" media="screen" rel="Stylesheet" type="text/css" />',
                         stylesheet_link_tag('style'))
        self.assertEqual('<link href="/dir/file.css" media="all" rel="Stylesheet" type="text/css" />',
                         stylesheet_link_tag('/dir/file', media='all'))
        self.assertEqual('<link href="/stylesheets/dir/file.css" media="screen" rel="Stylesheet" type="text/css" />',
                         stylesheet_link_tag('dir/file'))
        self.assertEqual('<link href="/stylesheets/style.css" media="all" rel="Stylesheet" type="text/css" />',
                         stylesheet_link_tag('style', media='all'))
        self.assertEqual('<link href="/stylesheets/random.styles" media="screen" rel="Stylesheet" type="text/css" />\n<link href="/css/stylish.css" media="screen" rel="Stylesheet" type="text/css" />',
                         stylesheet_link_tag('random.styles', '/css/stylish'))

if __name__ == '__main__':
    suite = [unittest.makeSuite(TestAssetTagHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
