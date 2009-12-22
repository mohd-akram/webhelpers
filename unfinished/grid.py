from routes.util import url_for
from webhelpers.html.builder import HTML, literal

class Grid(object):
    
    def default_column_format(self,i,record,column_name):
        return HTML.tag('td', record[column_name])
    
    def numbered_column_format(self,i,record):
        return HTML.tag('td', i)
    
    def default_record_format(self, i, record, class_name, columns):
        return HTML.tag('tr', columns,class_=class_name)

    def default_record_format(self, i, record, class_name, columns):
        return HTML.tag('tr', columns,class_=class_name)

    def default_header_record_format(self, headers):
        return HTML.tag('tr', headers,class_='header')

    def default_header_ordered_column_format(self, column_number, order, header_label):
        header_label = HTML(header_label,HTML.tag('span',class_='marker'))
        class_name = 'column%s ordering' % (column_number)
        return HTML.tag('td', header_label, class_=class_name)

    def default_header_column_format(self, column_number, header_label):
        class_name = 'column%s' % (column_number)
        return HTML.tag('td', header_label, class_=class_name)
    
    def default_header_link(self,url,content):
        return HTML.tag("a", href=url, c=content)
    
    def __init__(self, itemlist, columns=None, order_by=None, format=None,
        start_number=1):
        self.custom_record_format = None
        
        self.labels = {}
        self.exclude_ordering = ['_numbered']
        self.itemlist = itemlist
        if '_numbered' in columns:
            self.labels['_numbered'] = 'no.'            
        self.columns = columns
        self.order_column = order_by
        self.format = format or {}
        self._start_number = start_number

    def make_headers(self):
        header_columns = []
        for i, column in enumerate(self.columns):
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
                label_text = self.default_header_link(url_for(order_by=new_ordering, **request_copy.GET), label_text)
                #lets test if the column we try to order on is this column
                if self.order_column and column == self.order_column[0:-4] and self.order_column[-3:] == 'asc':
                    header_columns.append(self.default_header_ordered_column_format(i+1,'asc', label_text))
                elif self.order_column and column == self.order_column[0:-4] and self.order_column[-3:] == 'dsc':
                    header_columns.append(self.default_header_ordered_column_format(i+1,'dsc', label_text))
                else:
                    header_columns.append(self.default_header_column_format(i+1,label_text))    
            else:
                header_columns.append(self.default_header_column_format(i+1,label_text))
        return HTML(*header_columns)
    
    def make_columns(self, i, record):
        columns = []
        if '_numbered' in self.columns:
            columns.append(self.numbered_column_format(i + self._start_number, record))
            for column in self.columns[1:]:
                if column in self.format:
                    pass
                    columns.append(self.format[column](i, record))
                else:
                    columns.append(self.default_column_format(i, record, column))     
        else:
            for i,column in enumerate(self.columns):
                if column in self.format:
                    columns.append(self.format[column](i, record))
                else:
                    columns.append(self.default_column_format(i, record, column)) 
        return HTML(*columns)
    
    def __html__(self):
        ''' renders the grid '''
        records = []
        #first render headers record
        records.append(self.default_header_record_format(self.make_headers()))
        for i, record in enumerate(self.itemlist):
            if i % 2 == 0:
                class_name = 'even'
            else:
                class_name = 'odd'
            if self.custom_record_format is None:
                records.append(self.default_record_format(i, record, class_name,self.make_columns(i, record)))
            else:
                records.append(self.custom_record_format(i, record, class_name, self.make_columns(i, record)))

        return HTML(*records)
    
    __str__ = __html__
