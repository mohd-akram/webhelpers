import grid
import grid_pylons
from webhelpers.html.builder import HTML, literal

test_data = [
             {'group_name':'foo','options':'lalala'},
             {'group_name':'foo2','options':'lalala2'},
             {'group_name':'foo3','options':'lalala3'},
             {'group_name':'foo4','options':'lalala4'},
             ]

test_grid = grid.Grid(test_data, columns=['_numbered','group_name','options'])
test_grid.exclude_ordering = ['options']
test_grid.format = {
'options':lambda i,item: HTML.tag('td', 'baz')
}


print '<table>'
print test_grid
print '/<table>'