from webhelpers.html import HTML, literal
import webhelpers.html.grid as grid
import webhelpers.pylonslib.grid_pylons as grid_pylons

def options_td(col_num, i, item):
    return HTML.td("baz", class_="c%s" % (col_num))

test_data = [
     {"group_name": "foo", "options": "lalala"},
     {"group_name": "foo2", "options": "lalala2"},
     {"group_name": "foo3", "options": "lalala3"},
     {"group_name": "foo4", "options": "lalala4"},
     ]

test_grid = grid.Grid(test_data, columns=["_numbered","group_name","options"])
test_grid.exclude_ordering = test_grid.columns
test_grid.format = {
    "options": options_td,
    }

print "<table>"
print test_grid
print "</table>"
