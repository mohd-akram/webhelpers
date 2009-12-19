import datetime

from nose.tools import eq_

import webhelpers.feedgenerator as fg

def test_simple_feed():
    pubdate = datetime.datetime(2009, 12, 18, 23, 45, 12)
    feed = fg.Rss201rev2Feed(
        title=u"Poynter E-Media Tidbits",
        link=u"http://www.poynter.org/column.asp?id=31",
        description=u"A group weblog by the sharpest minds in online media/journalism/publishing.",
        language=u"en",
    )
    feed.add_item(
        title="Hello", 
        link=u"http://www.holovaty.com/test/",
        description="Testing.",  
        pubdate=pubdate)
    result = feed.writeString("utf-8")
    control = """<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel><title>Poynter E-Media Tidbits</title><link>http://www.poynter.org/column.asp?id=31</link><description>A group weblog by the sharpest minds in online media/journalism/publishing.</description><language>en</language><lastBuildDate>Fri, 18 Dec 2009 23:45:12 -0000</lastBuildDate><item><title>Hello</title><link>http://www.holovaty.com/test/</link><description>Testing.</description><pubDate>Fri, 18 Dec 2009 23:45:12 -0000</pubDate></item></channel></rss>"""
    eq_(result, control)
