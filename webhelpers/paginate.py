"""
Paginate module for lists and ORMs.

This module helps dividing large lists of items into pages. The user 
is shown one page at a time and can navigate to other pages. Imagine you 
are offering a company phonebook and let the user search the entries. If 
the search result contains 23 entries but you may want to display no 
more than 10 entries at once. The first page contains entries 1-10, the 
second 11-20 and the third 21-23. See the documentation of the "Page" 
class for more information. 

This module is especially useful for Pylons web framework applications.

Compatibility warning:

This pagination module is an alternative to the deprecated pagination 
module. It is in no way compatible so just replacing the import 
statements will break your code.

This version of paginate was originally based on the 0.3.3 version from
http://workaround.org/cgi-bin/hg-paginate.

Additional documentation is in webhelpers/docs/paginate.txt.  

This software can be used under the terms of the MIT license:

Copyright (c) 2007,2008 Christoph Haas <email@christoph-haas.de>

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to 
the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

"""

import logging
import re
# Use templating for the .pager() [available since Python 2.4]
from string import Template
import warnings

# Import the webhelpers to create URLs
import webhelpers
from webhelpers.html import literal, HTML

# FIXME - webhelpers.rails.* is DEPRECATED
from webhelpers.rails.prototype import link_to_remote as get_link_to_remote
from webhelpers.rails.urls import link_to as get_link_to
from routes import url_for

__version__ = '0.3.3'
__author__ = 'Christoph Haas <email@christoph-haas.de>'

log = logging.getLogger(__name__)

# import SQLAlchemy if available
try:
    import sqlalchemy
except ImportError:
    sqlalchemy_available = False
else:
    sqlalchemy_available = sqlalchemy.__version__

def get_wrapper(obj, sqlalchemy_session=None):
    """
    Auto-detect the kind of object and return a list/tuple
    to access items from the collection.
    
    """
    # See if the collection is a sequence
    if isinstance(obj, (list, tuple)):
        return obj
    # Is SQLAlchemy 0.4 available? (0.3 is not supported - sorry)
    if sqlalchemy_available.startswith('0.4'):
        # Is the collection a query?
        if isinstance(obj, sqlalchemy.orm.query.Query):
            return _SQLAlchemyQuery(obj)

        # Is the collection an SQLAlchemy select object?
        if isinstance(obj, sqlalchemy.sql.expression.CompoundSelect) \
        or isinstance(obj, sqlalchemy.sql.expression.Select):
            return _SQLAlchemySelect(obj, sqlalchemy_session)

    raise TypeError("Sorry, your collection type is not supported by the paginate module. "
            "You can either provide a list, a tuple, an SQLAlchemy table or an "
            "SQLAlchemy query object.")

class _SQLAlchemySelect(object):
    
    """
    Iterable that allows to get slices from an SQLAlchemy Select object.
    """
    
    def __init__(self, obj, sqlalchemy_session=None):
        if not isinstance(sqlalchemy_session, sqlalchemy.orm.scoping.ScopedSession):
            raise TypeError("If you want to page an SQLAlchemy 'Table' object then you "
                    "have to provide a 'sqlalchemy_session' argument. See also: "
                    "http://www.sqlalchemy.org/docs/04/session.html")

        self.sqlalchemy_session = sqlalchemy_session
        self.obj = obj

    def __getitem__(self, range):
        if not isinstance(range, slice):
            raise Exception, "__getitem__ without slicing not supported"
        offset = range.start
        limit = range.stop - range.start
        select = self.obj.offset(offset).limit(limit)
        return self.sqlalchemy_session.execute(select).fetchall()

    def __len__(self):
        return self.sqlalchemy_session.execute(self.obj).rowcount

class _SQLAlchemyQuery(object):
    
    """Iterable that allows to get slices from an SQLAlchemy Query object."""
    
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, range):
        if not isinstance(range, slice):
            raise Exception, "__getitem__ without slicing not supported"
        return self.obj[range]

    def __len__(self):
        return self.obj.count()


# Since the items on a page are mainly a list we subclass the "list" type
class Page(list):
    
    """
    A list/iterator of items representing one page in a larger collection.

    An instance of the "Page" class is created from a collection of things. 
    The instance works as an iterator running from the first item to the 
    last item on the given page. The collection can be:

    - a sequence
    - an SQLAlchemy query
    - an SQLAlchemy table

    A "Page" instance maintains pagination logic associated with each 
    page, where it begins, what the first/last item on the page is, etc. 
    The pager() method creates a link list allowing the user to go to
    other pages.

    **WARNING:** Unless you pass in an item_count, a count will be 
    performed on the collection every time a Page instance is created. 
    If using an ORM, it's advised to pass in the number of items in the 
    collection if that number is known.

    Instance attributes:

    original_collection
        Points to the collection object being paged through

    item_count
        Number of items in the collection

    current_page
        Number of the current page

    items_per_page
        Maximal number of items displayed on a page

    first_page
        Number of the first page - starts with 1

    last_page
        Number of the last page

    page_count
        Number of pages

    items
        Sequence/iterator of items on the current page

    first_item
        Index of first item on the current page

    last_item
        Index of last item on the current page
        
    """
    
    def __init__(self, collection, current_page=1, items_per_page=20,
        item_count=None, sqlalchemy_session=None, *args, **kwargs):
        """
        Create a "Page" instance.

        Parameters:

        collection
            Sequence, SQLAlchemy table or SQLAlchemy query
            representing the collection of items to page through.

        current_page
            The requested page number - starts with 1. Default: 1.

        items_per_page
            The maximal number of items to be displayed per page.
            Default: 20.

        item_count (optional)
            The total number of items in the collection - if known.
            If this parameter is not given then the paginator will count
            the number of elements in the collection every time a "Page"
            is created. Giving this parameter will speed up things.

        sqlalchemy_session (optional)
            If you want to use an SQLAlchemy (0.4) table as a collection
            then you need to provide a Session. A 'Table'
            object does not have a database connection attached so the paginator
            wouldn't be able to execute a SELECT query without it.

        Further parameters are used as link arguments in the pager().
        
        """
        # 'page_nr' is deprecated. 'current_page' is clearer and used by Ruby-on-Rails, too
        if 'page_nr' in kwargs:
            warnings.warn("'page_nr' is deprecated. Please use current_page instead.")
            current_page = kwargs['page_nr']
            del kwargs['page_nr']

        # Safe the kwargs class-wide so they can be used in the pager() method
        self.kwargs = kwargs

        # Save a reference to the collection
        self.original_collection = collection

        # Decorate the ORM/sequence object with __getitem__ and __len__
        # functions to be able to get slices.
        if collection:
            # Determine the type of collection and use a wrapper for ORMs
            self.collection = get_wrapper(collection, sqlalchemy_session)
        else:
            self.collection = []

        # The self.current_page is the number of the current page.
        # The first page has the number 1!
        try:
            self.current_page = int(current_page) # make it int() if we get it as a string
        except ValueError:
            self.current_page = 1

        self.items_per_page = items_per_page

        # Unless the user tells us how many items the collections has
        # we calculate that ourselves.
        if item_count:
            self.item_count = item_count
        else:
            self.item_count = len(self.collection)

        # Compute the number of the first and last available page
        if self.item_count > 0:
            self.first_page = 1
            self.page_count = ((self.item_count - 1) / self.items_per_page) + 1
            self.last_page = self.first_page + self.page_count - 1

            # Make sure that the requested page number is the range of valid pages
            if self.current_page > self.last_page:
                self.current_page = self.last_page
            elif self.current_page < self.first_page:
                self.current_page = self.first_page

            # Note: the number of items on this page can be less than
            #       items_per_page if the last page is not full
            self.first_item = (self.current_page - 1) * items_per_page
            self.last_item = min(self.first_item + items_per_page - 1, self.item_count - 1)

            # We subclassed "list" so we need to call its init() method
            # and fill the new list with the items to be displayed on the page.
            # Using list() so that the collection is evaluated only once.
            # Otherwise it would run the actual SQL query everytime .items
            # would be accessed.
            self.items = list(self.collection[self.first_item:self.last_item+1])

            # Links to previous and next page
            if self.current_page > self.first_page:
                self.previous_page = self.current_page-1
            else:
                self.previous_page = None

            if self.current_page < self.last_page:
                self.next_page = self.current_page+1
            else:
                self.next_page = None

        # No items available
        else:
            self.first_page = None
            self.page_count = 0
            self.last_page = None
            self.first_item = None
            self.last_item = None
            self.previous_page = None
            self.next_page = None
            self.items = []

        # This is a subclass of the 'list' type. Initialise the list now.
        list.__init__(self, self.items)


    def __repr__(self):
        return ("Page:\n"
            "Collection type:  %(type)s\n"
            "Current page:     %(current_page)s\n"
            "First item:       %(first_item)s\n"
            "Last item:        %(last_item)s\n"
            "First page:       %(first_page)s\n"
            "Last page:        %(last_page)s\n"
            "Previous page:    %(previous_page)s\n"
            "Next page:        %(next_page)s\n"
            "Items per page:   %(items_per_page)s\n"
            "Number of items:  %(item_count)s\n"
            "Number of pages:  %(page_count)s\n"
            % {
            'type':type(self.collection),
            'current_page':self.current_page,
            'first_item':self.first_item,
            'last_item':self.last_item,
            'first_page':self.first_page,
            'last_page':self.last_page,
            'items_per_page':self.items_per_page,
            'item_count':self.item_count,
            'page_count':self.page_count,
            })

    def pager(self, format='~2~', link_var='page_nr', partial_var='partial',
        show_if_single_page=False, separator=' ',
        ajax_id=None, framework='scriptaculous',
        symbol_first='&lt;&lt;', symbol_last='&gt;&gt;',
        symbol_previous='&lt;', symbol_next='&gt;',
        link_attr={'class':'pager_link'}, curpage_attr={'class':'pager_curpage'},
        dotdot_attr={'class':'pager_dotdot'}, **kwargs):
        """
        Return string with links to other pages (e.g. "1 2 [3] 4 5 6 7").

        format:
            Format string that defines how the pager is rendered. The string
            can contain the following $-tokens that are substituted by the
            string.Template module:

            - $first_page: number of first reachable page
            - $last_page: number of last reachable page
            - $current_page: number of currently selected page
            - $page_count: number of reachable pages
            - $items_per_page: maximal number of items per page
            - $first_item: index of first item on the current page
            - $last_item: index of last item on the current page
            - $item_count: total number of items
            - $link_first: link to first page (unless this is first page)
            - $link_last: link to last page (unless this is last page)
            - $link_previous: link to prev page (unless this is first page)
            - $link_next: link to next page (unless this is last page)

            To render a range of pages the token '~3~' can be used. The 
            number sets the radius of pages around the current page.
            Example for a range with radius 3: 
               '1 .. 5 6 7 [8] 9 10 11 .. 500'

            Default: '~2~'

        symbol_first
            String to be displayed as the text for the %(link_first)s 
            link above.

            Default: '&lt;&lt;' ('<<')

        symbol_last
            String to be displayed as the text for the %(link_last)s 
            link above.

            Default: '&gt;&gt;' ('>>')

        symbol_previous
            String to be displayed as the text for the %(link_previous)s 
            link above.

            Default: '&lt;' ('<')

        symbol_next
            String to be displayed as the text for the %(link_next)s 
            link above.

            Default: '&gt;' ('>')

        separator:
            String that is used to seperate page links/numbers in the 
            above range of pages.

            Default: ' '

        link_var:
            The name of the parameter that will carry the number of the 
            page the user just clicked on. The parameter will be passed 
            to a url_for() call so if you stay with the default 
            ':controller/:action/:id' routing and set link_var='id' then 
            the :id part of the URL will be changed. If you set 
            link_var='current_page' then url_for() will make it an extra 
            parameters like ':controller/:action/:id?current_page=1'. 
            You need the link_var in your action to determine the page 
            number the user wants to see. If you do not specify anything 
            else the default will be a parameter called 'current_page'.

        partial_var:
            The name of the parameter that is set to 1 if updates of the 
            page area through AJAX/AJAH are requested. If your 
            application finds this parameter in the URL set then it 
            should not print the complete HTML page but just the page 
            area instead.

            Default: 'partial'

        show_if_single_page:
            if True the navigator will be shown even if there is only 
            one page
            
            Default: False

        link_attr (optional)
            A dictionary of attributes that get added to A-HREF links 
            pointing to other pages. Can be used to define a CSS style 
            or class to customize the look of links.

            Example: { 'style':'border: 1px solid green' }

            Default: { 'class':'pager_link' }

        curpage_attr (optional)
            A dictionary of attributes that get added to the current 
            page number in the pager (which is obviously not a link).
            If this dictionary is not empty then the elements
            will be wrapped in a SPAN tag with the given attributes.

            Example: { 'style':'border: 3px solid blue' }

            Default: { 'class':'pager_curpage' }

        dotdot_attr (optional)
            A dictionary of attributes that get added to the '..' string
            in the pager (which is obviously not a link). If this 
            dictionary is not empty then the elements will be wrapped in 
            a SPAN tag with the given attributes.

            Example: { 'style':'color: #808080' }

            Default: { 'class':'pager_dotdot' }

        ajax_id (optional)
            If this parameter is given then the navigator will add 
            Javascript to the A-HREF links that will update only a 
            portion of the web page instead of reloading the copmlete 
            page.

            This parameter contains the name of the HTML element (e.g. a 
            <div id="foobar">) that the paginator should replace with 
            the new content. The navigator will create AJAX links (e.g. 
            using  webhelpers' link_to_remote() function) that replace 
            the HTML element's content with the new page of paginated 
            items and a new navigator.

        framework
            The name of the Javascript framework to use. By default
            the AJAX functions from script.aculo.us are used. Supported
            Javascript frameworks:

            - scriptaculous (Default - script.aculo.us)
            - jquery (www.jquery.com)
            - yui (Yahoo UI library - developer.yahoo.com/yui/)
            - extjs (www.extjs.com)

        Additional keyword arguments are used as arguments in the links.
        Otherwise the link will be created with url_for() which points 
        to the page you are currently displaying.
        
        """

        def _pagerlink(pagenr, text):
            """
            Create a URL that links to another page using url_for().

            Parameters:
                
            pagenr
                Number of the page that the link points to

            text
                Text to be printed in the A-HREF tag
                
            """
            # Let the url_for() from webhelpers create a new link and set
            # the variable called 'link_var'. Example:
            # You are in '/foo/bar' (controller='foo', action='bar')
            # and you want to add a parameter 'pagenr'. Then you
            # call the navigator method with link_var='pagenr' and
            # the url_for() call will create a link '/foo/bar?pagenr=...'
            # with the respective page number added.
            link_params = {}
            # Use the instance kwargs from Page.__init__ as URL parameters
            link_params.update(self.kwargs)
            # Add keyword arguments from pager() to the link as parameters
            link_params.update(kwargs)
            link_params[link_var] = pagenr
            # Create the URL to load a certain page
            link_url = url_for(**link_params)
            log.debug("link_url(**%r) => %r", link_params, link_url)
            # Create the URL to load the page area part of a certain page (AJAX updates)
            link_params[partial_var] = 1
            partial_url = url_for(**link_params)
            log.debug("partial_url(**%r) => %r", link_params, partial_url)
            if ajax_id:
                # Return an AJAX link that will update the HTML element
                # named by ajax_id.
                # Degrade gracefully if Javascript is not available by using
                # 'partial_url' in the onclick URLs while using 'link_url'
                # in the A-HREF URL.
                if framework == 'scriptaculous':
                    return get_link_to_remote(text, dict(update=ajax_id, url=partial_url),
                        href=link_url, **link_attr)
                elif framework == 'jquery':
                    return get_link_to(text, url=link_url,
                        onclick="""$('#%s').load('%s'); return false""" % (ajax_id, partial_url),
                            **link_attr)
                elif framework == 'yui':
                    js = """YAHOO.util.Connect.asyncRequest('GET','%s',{
                        success:function(o){YAHOO.util.Dom.get('%s').innerHTML=o.responseText;}
                        },null); return false;""" % (partial_url, ajax_id)
                    return get_link_to(text, url=link_url, onclick=js, **link_attr)
                elif framework == 'extjs':
                    js = """Ext.get('%s').load({url:'%s'}); return false;""" % (ajax_id, partial_url)
                    return get_link_to(text, url=link_url, onclick=js, **link_attr)
                else:
                    raise Exception, "Unsupported Javascript framework: %s" % framework

            else:
                # Return a normal a-href link that will call the same
                # controller/action with the link_var set to the new
                # page number.
                return get_link_to(text, link_url, **link_attr)

        #------- end of def _pagerlink

        def _range(regexp_match):
            """
            Return range of linked pages (e.g. '1 2 [3] 4 5 6 7 8').

            Arguments:
                
            regexp_match
                A "re" (regular expressions) match object containing the
                radius of linked pages around the current page in
                regexp_match.group(1) as a string

            This funtion is supposed to be called as a callable in 
            re.sub.
            
            """
            radius = int(regexp_match.group(1))

            # Compute the first and last page number within the radius
            # e.g. '1 .. 5 6 [7] 8 9 .. 12'
            # -> leftmost_page  = 5
            # -> rightmost_page = 9
            leftmost_page = max(self.first_page, (self.current_page-radius))
            rightmost_page = min(self.last_page, (self.current_page+radius))

            nav_items = []

            # Create a link to the first page (unless we are on the first page
            # or there would be no need to insert '..' spacers)
            if self.current_page != self.first_page and self.first_page < leftmost_page:
                nav_items.append( _pagerlink(self.first_page, self.first_page) )

            # Insert dots if there are pages between the first page
            # and the currently displayed page range
            if leftmost_page - self.first_page > 1:
                # Wrap in a SPAN tag if nolink_attr is set
                text = '..'
                if dotdot_attr:
                    text = HTML.span(c=text, **dotdot_attr)
                nav_items.append(text)

            for thispage in xrange(leftmost_page, rightmost_page+1):
                # Hilight the current page number and do not use a link
                if thispage == self.current_page:
                    text = '%s' % (thispage,)
                    # Wrap in a SPAN tag if nolink_attr is set
                    if curpage_attr:
                        text = HTML.span(c=text, **curpage_attr)
                    nav_items.append(text)
                # Otherwise create just a link to that page
                else:
                    text = '%s' % (thispage,)
                    nav_items.append( _pagerlink(thispage, text) )

            # Insert dots if there are pages between the displayed
            # page numbers and the end of the page range
            if self.last_page - rightmost_page > 1:
                text = '..'
                # Wrap in a SPAN tag if nolink_attr is set
                if dotdot_attr:
                    text = HTML.span(c=text, **dotdot_attr)
                nav_items.append(text)

            # Create a link to the very last page (unless we are on the last
            # page or there would be no need to insert '..' spacers)
            if self.current_page != self.last_page and rightmost_page < self.last_page:
                nav_items.append( _pagerlink(self.last_page, self.last_page) )

            return separator.join(nav_items)

        #------- end of def _range


        # Don't show navigator if there is no more than one page
        if self.page_count == 0 or (self.page_count == 1 and not show_if_single_page):
            return ''


        # Replace ~...~ in token format by range of pages
        result = re.sub(r'~(\d+)~', _range, format)

        # Interpolate '%' variables
        result = Template(result).safe_substitute({
            'first_page': self.first_page,
            'last_page': self.last_page,
            'current_page': self.current_page,
            'page_count': self.page_count,
            'items_per_page': self.items_per_page,
            'first_item': self.first_item,
            'last_item': self.last_item,
            'item_count': self.item_count,
            'link_first': self.current_page>self.first_page and \
                    _pagerlink(self.first_page, symbol_first) or '',
            'link_last': self.current_page<self.last_page and \
                    _pagerlink(self.last_page, symbol_last) or '',
            'link_previous': self.previous_page and \
                    _pagerlink(self.previous_page, symbol_previous) or '',
            'link_next': self.next_page and \
                    _pagerlink(self.next_page, symbol_next) or ''
        })

        return result

