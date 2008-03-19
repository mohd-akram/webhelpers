from util import WebHelpersTestCase
import unittest

from webhelpers.asset_tag import *
from webhelpers.asset_tag import compute_public_path

class TestAssetTagHelper(WebHelpersTestCase):
    def test_auto_discovery_link_tag(self):
        self.assertEqual('<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />',
                         auto_discovery_link('http://feed.com/feed.xml'))
        self.assertEqual('<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />',
                         auto_discovery_link('http://feed.com/feed.xml', type='atom'))
        self.assertEqual('<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />',
                         auto_discovery_link('app.rss', type='atom', title='atom feed'))
        self.assertEqual('<link href="app.rss" rel="alternate" title="My RSS" type="application/rss+xml" />',
                         auto_discovery_link('app.rss', title='My RSS'))
        self.assertEqual('<link href="/app.rss" rel="alternate" title="" type="text/html" />',
                         auto_discovery_link('/app.rss', type='text/html'))
        self.assertEqual('<link href="/app.html" rel="alternate" title="My RSS" type="text/html" />',
                         auto_discovery_link('/app.html', title='My RSS', type='text/html'))
        
    def test_image(self):
        self.assertEqual('<img alt="Xml" src="/images/xml.png" />',
                         image('xml.png'))
        self.assertEqual('<img alt="rss syndication" src="/images/rss.png" />',
                         image('rss.png', alt='rss syndication'))
        self.assertEqual('<img alt="Gold" height="70" src="/images/gold.png" width="45" />',
                         image('gold.png', height=70, width=45))
        self.assertEqual('<img alt="Symbolize" height="70" src="/images/symbolize.jpg" width="45" />',
                         image('symbolize.jpg', height=70, width=45))
        self.assertEqual('<img alt="Pylons-Tower-Dark1" src="http://pylons.tgtg.org/powered/_img/pylons-tower-dark1.png" />',
                         image('http://pylons.tgtg.org/powered/_img/pylons-tower-dark1.png'))
        self.assertEqual('<img alt="Edit Entry" height="10" src="/images/icon.png" width="16" />',
                         image("icon.png", height=10, width=16, alt="Edit Entry"))
        self.assertEqual('<img alt="Icon" height="16" src="/icons/icon.gif" width="16" />',
                         image("/icons/icon.gif", height=16, width=16))
        self.assertEqual('<img alt="Icon" src="/icons/icon.gif" width="16" />',
                         image("/icons/icon.gif", width=16))

    def test_javascript_include_tag(self):
        self.assertEqual("""<script src="/javascripts/prototype.js" type="text/javascript"></script>\n<script src="/other-javascripts/util.js" type="text/javascript"></script>""",
                         javascript_link('prototype', '/other-javascripts/util.js'))
        self.assertEqual("""<script defer="defer" src="/js/pngfix.js" type="text/javascript"></script>""",
                         javascript_link('/js/pngfix.js', defer=True))
        self.assertEqual("""<script defer="defer" src="/js/pngfix.js" type="text/javascript"></script>""",
                         javascript_link('/js/pngfix.js', defer="defer"))

    def test_stylesheet_link_tag(self):
        self.assertEqual('<link href="/stylesheets/style.css" media="screen" rel="Stylesheet" type="text/css" />',
                         stylesheet_link('style'))
        self.assertEqual('<link href="/dir/file.css" media="all" rel="Stylesheet" type="text/css" />',
                         stylesheet_link('/dir/file', media='all'))
        self.assertEqual('<link href="/stylesheets/dir/file.css" media="screen" rel="Stylesheet" type="text/css" />',
                         stylesheet_link('dir/file'))
        self.assertEqual('<link href="/stylesheets/style.css" media="all" rel="Stylesheet" type="text/css" />',
                         stylesheet_link('style', media='all'))
        self.assertEqual('<link href="/stylesheets/random.styles" media="screen" rel="Stylesheet" type="text/css" />\n<link href="/css/stylish.css" media="screen" rel="Stylesheet" type="text/css" />',
                         stylesheet_link('random.styles', '/css/stylish'))
        self.assertEqual('<link href="/stylesheets/dir/file.css" media="all" rel="Stylesheet" type="text/css" />',
                         stylesheet_link('dir/file', media='all'))

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
