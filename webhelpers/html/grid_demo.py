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
from webhelpers.misc import subclasses_only
# XXX You may find other helpers in webhelpers.html.tags useful too

#### Global constants ####
USAGE = "python -m %s OUTPUT_DIRECTORY" % __name__

DESCRIPTION = """\
Run the demos in this module and put the HTML output in
OUTPUT_DIRECTORY."""

STYLESHEET = """\
/******************* tables ****************/
table.stylized {
    background-color: #ffffff;
    border-collapse: separate;
    border-spacing: 1px;
    border-bottom: 2px solid #666666;
    margin: 1px 5px 5px 5px;
    -moz-border-radius: 5px;
    -webkit-border-radius: 5px;
    width: 100%;
    border-collapse: collapse;
}

table.stylized caption {
    color: #ffffff;
    background-color: #444466;
    padding: 5px;
    font-size: 1.3em;
    font-weight: bold;
    margin: 5px 0px 0px 0px;
    -moz-border-radius: 5px;
    -webkit-border-radius: 5px;
}



table.stylized caption a:link,table.stylized caption a:visited{
    color: #ffffff;
    text-decoration: none;
    font-weight: bold;
}

table.stylized caption a:link,table.stylized caption a:hover{
    color: #ffcc00;
    text-decoration: none;
    font-weight: bold;
}
    
table.stylized thead {
    background-color: #ffffff;
}

table.stylized tbody {
    background-color: #ffffff;
}

table.stylized tfooter {
    background-color: #ffffff;
}

table.stylized th {
    text-align: center;
}

table.stylized tr.header {
    text-align: center;
}

table.stylized tr.header td, table.stylized th {
    text-align: center;
    color: #ffffff;
    background-color: #444466;
}

table.stylized td {
    padding: 5px 5px 5px 5px;
    border: 1px solid #dcdcdc;
}


table.stylized tr.odd td {
    border-top: 1px solid #999 !important;
    background-color: #ffffff;
}

table.stylized tr.even td {
    border-top: 1px solid #999 !important;
    background-color: #f6f6f6;
}

table.stylized .no {
    width: 30px;
}

table.stylized td.ordering.dsc {
    background-color: #666666;
    padding-right: 20px;
}

table.stylized td.ordering.asc {
    background-color: #666666;
    padding-right: 20px;
}

table.stylized td.ordering.dsc .marker {
    height: 20px;
    width: 20px;
    display: block;
    float: right;
    margin: 0px -18px;
}

table.stylized td.ordering.asc .marker {
    height: 20px;
    width: 20px;
    display: block;
    float: right;
    margin: 0px -18px;
}

table.stylized .header a:link,table.stylized .header a:visited {
    color: #ffffff;
    text-decoration: none;
    font-weight: bold;
}

table.stylized td.ordering a:link,table.stylized td.ordering a:visited {
    color: #ffcc00;
    text-decoration: none;
    font-weight: bold;
}
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

        <table class="stylized">
%(grid)s
        </table>

        <p>%(description)s</p>
    </body>
</html>
""")
# XXX There should be helpers to create a basic HTML file.

test_data = [
             {"group_name": "foo", "options": "lalala", "id":1},
             {"group_name": "foo2", "options": "lalala2", "id":2},
             {"group_name": "foo3", "options": "lalala3", "id":3},
             {"group_name": "foo4", "options": "lalala4", "id":4},
             ]

#### Demo base class ####
class _DemoBase(object):
    title = None
    description = None

    def get_grid(): 
        raise NotImplementedError("subclass responsibility")


#### Demo classes ###
class BasicDemo(_DemoBase):
    name = "Tickets"
    description = """\
This table shows a basic grid."""

    def get_grid(self):
        """
        basic demo
        """
        
        g = Grid(test_data, columns=["_numbered","group_name","options"])
        return g

#### Demo classes ###
class CustomColumnDemo(_DemoBase):
    name = "CustomColumn"
    description = """\
This table shows a grid with a customized column and header label."""

    def get_grid(self):
        """
        let's override how rows look like
        subject is link
        categories and status hold text based on param of item text , the
        translations are dicts holding translation strings correlated with
        integers from db, in this example
        """
        def options_td(col_num, i, item):
            # XXX This module can't depend on 'app_globals' or 'url' or
            # external data. Define data within this method or class or
            # in a base class.
            # Could use HTML.a() instead of link_to().
            u = url("/tickets/view", ticket_id=item["id"])
            a = link_to(item["options"], u)
            return HTML.td(a)
        
        g = Grid(test_data, columns=["_numbered","group_name","options"])
        g.labels["options"] = 'FOOBAAR'
        g.column_formats = {
            "options": options_td,
            }
        return g

demos = subclasses_only(_DemoBase, globals())

#demos = [BasicDemo, CustomColumnDemo]

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
        name = d.name or d.__class__.__name__
        filename = name + ".html"
        dic = {
            "title": d.name or d.__class__.__name__.lower(),
            "description": d.description,
            "grid": d.get_grid(),
            }
        html = HTML_TEMPLATE % dic
        write_file(dir, filename, html)

if __name__ == "__main__":  main()
