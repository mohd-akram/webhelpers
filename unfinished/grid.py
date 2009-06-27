from routes.util import url_for
from pylons import request

class Grid(object):
    
    def __init__(self, itemlist, *args, **kwargs):
        self.default_column_format = '\n\t<td>%s</td>'
        self.default_row_format = '\n\t<tr class="%s">%s</tr>'
        self.custom_row_format = None
        self.default_header_row_format = '\n<tr class="header">\n%s\n</tr>'
        self.default_header_ordered_column_format = '<td class="column%s ordering %s">%s<span class="marker"></span></td>'
        self.default_header_column_format = '<td class="column%s">%s</td>'
        self.default_header_link = '<a href="%s">%s</a>'
        
        self.labels = {}
        self.exclude_ordering = ['_numbered']
        self.itemlist = itemlist
        columns = kwargs['columns']
        if '_numbered' in columns:
            self.labels['_numbered'] = 'no.'            
        self.columns = columns
        if 'format' in kwargs:
            self.format = kwargs['format']
        else:
            self.format = {}
        if 'start_number' in kwargs:
            self._start_number = kwargs['start_number']
        else:
            self._start_number = 1

    def __make_header_columns(self):
        header_columns = []
        request_copy = request.copy()
        if 'order_by' in request_copy.GET:
            self.order_column = request_copy.GET.pop('order_by')
        else:
            self.order_column = None
            
        for i,column in enumerate(self.columns):
            #lets generate header column contents
            label_text = ''
            if column in self.labels:
                label_text = self.labels[column]
            else:
                label_text = column.replace('_', ' ').title()
            if column not in self.exclude_ordering:
                if self.order_column and column == self.order_column[0:-4] and self.order_column[-3:] == 'asc':
                    new_ordering = column + '_dsc'
                else:
                    new_ordering = column + '_asc'
                label_text = self.default_header_link % (url_for(order_by=new_ordering, **request_copy.GET), label_text)
                #lets test if the column we try to order on is this column
                if self.order_column and column == self.order_column[0:-4] and self.order_column[-3:] == 'asc':
                    header_columns.append(self.default_header_ordered_column_format % (i+1,'asc', label_text))
                elif self.order_column and column == self.order_column[0:-4] and self.order_column[-3:] == 'dsc':
                    header_columns.append(self.default_header_ordered_column_format % (i+1,'dsc', label_text))
                else:
                    header_columns.append(self.default_header_column_format % (i+1,label_text))    
            else:
                header_columns.append(self.default_header_column_format % (i+1,label_text))
        return ''.join(header_columns)
    
    def __make_columns(self, i, row):
        columns = []
        if '_numbered' in self.columns:
            columns.append(self.default_column_format % (i + self._start_number))
            for column in self.columns[1:]:
                if column in self.format:
                    pass
                    columns.append(self.format[column](i, row))
                else:
                    columns.append(self.default_column_format % row[column])        
        else:
            for i,column in enumerate(self.columns):
                if column in self.format:
                    pass
                    columns.append(self.format[column](i, row))
                else:
                    columns.append(self.default_column_format % row[column]) 
        return ''.join(columns)
    
    def render(self):
        ''' renders the grid '''
        rows = []
        #first render headers row
        rows.append(self.default_header_row_format % self.__make_header_columns())
        if self.custom_row_format is None:
            for i, row in enumerate(self.itemlist):
                if i % 2 == 0:
                    class_name = 'even'
                else:
                    class_name = 'odd'
                rows.append(self.default_row_format % (class_name,self.__make_columns(i, row)))
        else:
            for i, row in enumerate(self.itemlist):
                if i % 2 == 0:
                    class_name = 'even'
                else:
                    class_name = 'odd'
                rows.append(self.custom_row_format(class_name,i, row, self.__make_columns(i, row)))
        return ''.join(rows)
