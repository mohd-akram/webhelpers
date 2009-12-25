from webhelpers.html.builder import HTML, literal
import webhelpers.html.grid as grid

class NoRequestException(Exception):
    pass

class GridPylons(grid.Grid):
    
    def generate_header_link(self, column_number, column, label_text):
        from pylons import request, url

        # this will handle possible URL generation
        if not hasattr(self, "request"):
            raise NoRequestException(
                "Could not find self.request for this grid")
        request_copy = self.request.copy().GET
        if "order_by" in request_copy:
            self.order_column = request_copy.pop("order_by")
        else:
            self.order_column = None
            
        if (self.order_column and column == self.order_column[0:-4] and 
            self.order_column[-3:] == "asc"):
            new_ordering = column + "_dsc"
        else:
            new_ordering = column + "_asc"
        url_href = url(order_by=new_ordering, **request_copy)        
        label_text = HTML.tag("a", href=url_href, c=label_text)
        # Is the current column the one we're ordering on?
        if (self.order_column and column == self.order_column[0:-4] and 
            self.order_column[-3:] == "asc"):
            return self.default_header_ordered_column_format(i, "asc", column, 
                label_text)
        elif (self.order_column and column == self.order_column[0:-4] and 
            self.order_column[-3:] == "dsc"):
            return self.default_header_ordered_column_format(i, "dsc", column, 
                label_text)
        else:
            return self.default_header_column_format(i, column, label_text)
        
