from webhelpers.html.builder import HTML, literal

class Grid(object):
    
    def __init__(self, itemlist, *args, **kwargs):
        self.custom_record_format = None
        self.labels = {}
        self.exclude_ordering = ["_numbered"]
        self.itemlist = itemlist
        columns = kwargs["columns"]
        if "_numbered" in columns:
            self.labels["_numbered"] = "no."
        self.columns = columns
        self.format = kwargs.get("format", {})
        self._start_number = kwargs.get("start_number", 1)
        

    def make_headers(self):
        header_columns = []
            
        for i, column in enumerate(self.columns):
            # let"s generate header column contents
            label_text = ""
            if column in self.labels:
                label_text = self.labels[column]
            else:
                label_text = column.replace("_", " ").title()
            # handle non clickable columns
            if column in self.exclude_ordering:
                header = self.default_header_column_format(i + 1, column, label_text)
            # handle clickable columns
            else:
                header = self.generate_header_link(i + 1, column, label_text)
                if header is None:
                    header = self.default_header_column_format(i + 1, column, label_text)                    
            header_columns.append(header)               
        return HTML(*header_columns)
    
    def make_columns(self, i, record):
        columns = []        
        for col_num, column in enumerate(self.columns):
            if column in self.format:
                columns.append(self.format[column](col_num, i, record))
            else:
                if column == "_numbered":
                    columns.append(self.numbered_column_format(col_num, i + self._start_number, record))
                else:
                    columns.append(self.default_column_format(col_num, i, record, column)) 
        return HTML(*columns)
    
    def __html__(self):
        """ renders the grid """
        records = []
        #first render headers record
        records.append(self.default_header_record_format(self.make_headers()))
        for i, record in enumerate(self.itemlist):
            if i % 2 == 0:
                class_name = "even"
            else:
                class_name = "odd"
            if self.custom_record_format is None:
                records.append(self.default_record_format(i, record, class_name, self.make_columns(i, record)))
            else:
                records.append(self.custom_record_format(i, record, class_name, self.make_columns(i, record)))

        return HTML(*records)
    
    def __str__(self):
        return self.__html__()

    def generate_header_link(self, column_number, column, label_text):
        return None

    #### Default HTML tag formats ####

    def default_column_format(self, column_number, i, record, column_name):
        class_name = "c%s" % (column_number)
        return HTML.tag("td", record[column_name], class_=class_name)
    
    def numbered_column_format(self, column_number, i, record):
        class_name = "c%s" % (column_number)
        return HTML.tag("td", i, class_=class_name)
    
    def default_record_format(self, i, record, class_name, columns):
        return HTML.tag("tr", columns, class_=class_name)

    def default_record_format(self, i, record, class_name, columns):
        return HTML.tag("tr", columns, class_=class_name)

    def default_header_record_format(self, headers):
        return HTML.tag("tr", headers, class_="header")

    def default_header_ordered_column_format(self, column_number, order, column_name, header_label):
        header_label = HTML(header_label, HTML.tag("span", class_="marker"))
        if column_name == "_numbered":
            column_name = "numbered"
        class_name = "c%s ordering %s %s" % (column_number, order, column_name)
        return HTML.tag("td", header_label, class_=class_name)

    def default_header_column_format(self, column_number, column_name, header_label):
        if column_name == "_numbered":
            column_name = "numbered"
        class_name = "c%s %s" % (column_number, column_name)
        return HTML.tag("td", header_label, class_=class_name)
    
