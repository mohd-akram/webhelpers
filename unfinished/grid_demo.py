"""Demos for webhelpers.html.grid

Run this module as a script::

    python -m webhelpers.html.grid_demo OUTPUT_DIRECTORY
 Dec 16 19:39:54 PST 2009
"""

import optparse
import os
import urllib

from webhelpers.html import *
from webhelpers.html.grid import Grid
from webhelpers.html.tags import link_to
# XXX You may find other helpers in webhelpers.html.tags useful too

#### Global constants ####
USAGE = "python -m %s OUTPUT_DIRECTORY" % __name__

DESCRIPTION = """\
Run the demos in this module and put the HTML output in
OUTPUT_DIRECTORY."""

STYLESHEET = """\
/* Put styles here. */
"""

HTML_TEMPLATE = literal("""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <title>%(title)s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="demo.css" />
    </head>
    <body>
        <h1>%(title)s</h1>

        <table>
%(grid)s
        </table>

        <p>%(description)s</p>
    </body>
</html>
""")
# XXX There should be helpers to create a basic HTML file.

#### Demo base class ####
class _DemoBase(object):
    title = None
    description = None

    def get_grid(): 
        raise NotImplementedError("subclass responsibility")


#### Demo classes ###
class TicketsDemo(_DemoBase):
    title = "Tickets"
    description = """\
This table shows [XXX mention features]."""

    def get_grid(self):
        """
        lets override how rows look like
        subject is link
        categories and status hold text based on param of item text , the
        translations are dicts holding translation strings correlated with
        integers from db, in this example
        """
        columns = ['_numbered','subject','category','status','date']
        g = Grid(c.tickets, columns=columns)
        g.format = {
            "subject": self.subject,
            "category": self.category,
            "status": self.status,
            # XXX What about 'Date' column?
            }
        return g

    def subject(self, i, item):
        # XXX This module can't depend on 'app_globals' or 'url' or
        # external data. Define data within this method or class or
        # in a base class.
        # Could use HTML.a() instead of link_to().
        u = url("/tickets/view", ticket_id=item["id"])
        a = link_to(item["subject"], u)
        return HTML.td(a)

    def category(self, i, item):
        return HTML.td(item["category"])

    def status(self, i, item):
        return HTML.td(item["status"])


demos = [x for x in globals().iteritems() if
    isinstance(x, _DemoBase) and x is not _DemoBase]

#### Utility functions ####
def url(urlpath, **params):
    # This should be a helper and I think it's defined somewhere but I
    # can't think of where.
    return urlpath + "?" + urllib.urlencode(params)

def write_file(dir, filename, content):
    print "... writing '%s'" % filename
    path = os.path.join(dir, filename)
    f = open(path, "w")
    f.write(content)
    f.close()

#### Main routine ####
def main():
    parser = optparse.OptionParser(usage=USAGE, description=DESCRIPTION)
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error("wrong number of command-line arguments")
    dir = args[0]
    if not os.path.exists(dir):
        os.makedirs(dir)
    print "Putting output in directory '%s'" % dir
    write_file(dir, "demo.css", STYLESHEET)
    for class_ in demos:
        d = class_()
        title = d.name or d.__class__.__name__
        filename = name + ".html"
        dic = {
            "title": d.name or d.__class__.__name__.lower(),
            "description": d.description,
            "grid": d.get_grid(),
            }
        html = HTML_TEMPLATE % dic
        write_file(dir, filename, html)

if __name__ == "__main__":  main()
