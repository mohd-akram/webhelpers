from unittest import TestCase
import unittest

from webhelpers.rails.asset_tag import *
from webhelpers.rails.asset_tag import compute_public_path

class TestAssetTagHelper(TestCase):
    def test_auto_discovery_link_tag(self):
        self.assertEqual('<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />',
                         auto_discovery_link_tag('http://feed.com/feed.xml'))
        self.assertEqual('<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />',
                         auto_discovery_link_tag('http://feed.com/feed.xml', type='atom'))
        self.assertEqual('<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />',
                         auto_discovery_link_tag('app.rss', type='atom', title='atom feed'))
        self.assertEqual('<link href="app.rss" rel="alternate" title="My RSS" type="application/rss+xml" />',
                         auto_discovery_link_tag('app.rss', title='My RSS'))
        self.assertEqual('<link href="/app.rss" rel="alternate" title="" type="text/html" />',
                         auto_discovery_link_tag('/app.rss', type='text/html'))
        self.assertEqual('<link href="/app.html" rel="alternate" title="My RSS" type="text/html" />',
                         auto_discovery_link_tag('/app.html', title='My RSS', type='text/html'))
        
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

    def test_compute_public_path(self):
        self.assertEqual('/test.js', compute_public_path('/test.js'))
        self.assertEqual('/test.js', compute_public_path('/test.js', 'javascripts'))
        self.assertEqual('test.js', compute_public_path('test.js'))
        self.assertEqual('test.js', compute_public_path('test', ext='js'))
        self.assertEqual('/javascripts/test.js',
                         compute_public_path('test.js', 'javascripts'))
        self.assertEqual('/javascripts/test.js',
                         compute_public_path('test', 'javascripts', 'js'))
        self.assertEqual('/javascripts/test.js',
                         compute_public_path('test.js', 'javascripts', 'js'))
        self.assertEqual('http://www.pylonshq.com',
                         compute_public_path('http://www.pylonshq.com'))
        self.assertEqual('http://www.pylonshq.com',
                         compute_public_path('http://www.pylonshq.com', 'javascripts'))
        self.assertEqual('http://www.pylonshq.com',
                         compute_public_path('http://www.pylonshq.com', 'javascripts', 'js'))
        self.assertEqual('mailto:bdfl@python.org',
                         compute_public_path('mailto:bdfl@python.org'))
        self.assertEqual('mailto:bdfl@python.org',
                         compute_public_path('mailto:bdfl@python.org', 'javascripts'))
        self.assertEqual('mailto:bdfl@python.org',
                         compute_public_path('mailto:bdfl@python.org', 'javascripts', 'js'))
        
if __name__ == '__main__':
    suite = [unittest.makeSuite(TestAssetTagHelper)]
    for testsuite in suite:
        unittest.TextTestRunner(verbosity=1).run(testsuite)
