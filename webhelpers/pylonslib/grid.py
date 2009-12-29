from webhelpers.html.builder import HTML, literal
import webhelpers.html.grid as grid

class NoRequestError(Exception):
    pass

class GridPylons(grid.Grid):
    
    def generate_header_link(self, column_number, column, label_text):
        from pylons import url
        # this will handle possible URL generation
        if not hasattr(self, "request"):
            raise NoRequestError(
                "Could not find self.request for this grid")
        request_copy = self.request.copy().GET
        if "order_col" in request_copy and "order_dir" in request_copy:
            self.order_column = request_copy.pop("order_col")
            self.order_dir = request_copy.pop("order_dir")
        else:
            self.order_column = None
            self.order_dir = None
            
        if (column == self.order_column and self.order_dir == "asc"):
            new_order_dir = "dsc"
        else:
            new_order_dir = "asc"
        
        url_href = url.current(order_col=column, order_dir=new_order_dir, **request_copy)        
        label_text = HTML.tag("a", href=url_href, c=label_text)
        # Is the current column the one we're ordering on?
        if (column == self.order_column):
            return self.default_header_ordered_column_format(column_number, self.order_dir,
                                                             column, label_text)
        else:
            return self.default_header_column_format(column_number, column, label_text)
