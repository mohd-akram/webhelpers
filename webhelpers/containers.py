"""Container objects and list/dict helpers.

I would have called this "collections" except that Python 2 can't import a
top-level module that's the same name as a module in the current package.
"""

import sys

try:
    from collections import defaultdict
except ImportError:   # Python < 2.5
    class defaultdict(dict):
        """Backport of Python 2.5's ``defaultdict``.

        From the Python Cookbook.  Written by Jason Kirtland.
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/523034
        """
        def __init__(self, default_factory=None, *a, **kw):
            if (default_factory is not None and
                not hasattr(default_factory, '__call__')):
                raise TypeError('first argument must be callable')
            dict.__init__(self, *a, **kw)
            self.default_factory = default_factory
        def __getitem__(self, key):
            try:
                return dict.__getitem__(self, key)
            except KeyError:
                return self.__missing__(key)
        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError(key)
            self[key] = value = self.default_factory()
            return value
        def __reduce__(self):
            if self.default_factory is None:
                args = tuple()
            else:
                args = self.default_factory,
            return type(self), args, None, None, self.items()
        def copy(self):
            return self.__copy__()
        def __copy__(self):
            return type(self)(self.default_factory, self)
        def __deepcopy__(self, memo):
            import copy
            return type(self)(self.default_factory,
                              copy.deepcopy(self.items()))
        def __repr__(self):
            return 'defaultdict(%s, %s)' % (self.default_factory,
                                            dict.__repr__(self))

class NoDefault(object):
    pass


class DumbObject(object):
    """A container for arbitrary attributes.

    Usage:
    >>> do = DumbObject(a=1, b=2)
    >>> do.b
    2
    
    Alternatives to this class include ``collections.namedtuple`` in Python
    2.6, and ``formencode.declarative.Declarative`` in Ian Bicking's FormEncode
    package.  Both alternatives offer more featues, but ``DumbObject``
    shines in its simplicity and lack of dependencies.
    """
    def __init__(self, **kw):
        self.__dict__.update(kw)


class Flash(object):
    """Accumulate a list of messages to show at the next page request.

    This class is useful when you want to redirect to another page and also
    show a status message on that page, such as "Changes saved" or 
    "No previous search found; returning to home page".

    THIS IMPLEMENTATION DEPENDS ON PYLONS.  However, it can easily be adapted
    for another web framework.

    Normally you instantiate a Flash object in myapp/lib/helpers.py:

        from webhelpers.tools import Flash as _Flash
        flash = _Flash()

    The helpers module is then imported into your controllers and
    templates as `h`.  Whenever you want to set a message, do this::

        h.flash("Record deleted.")

    You can set additional messages too::

        h.flash("Hope you didn't need it.")

    Now make a place in your site template for the messages.  In Mako you
    might do::

        <% messages = h.flash.pop_messages() %>
        % if messages:
        <ul id="flash-messages">
        % for message in messages:
            <li>${message}</li>
        % endfor
        </ul>
        % endif

    You can style this to look however you want::

        ul#flash-messages {
            color: red;
            background-color: #FFFFCC;
            font-size: larger;
            font-style: italic;
            margin-left: 40px;
            padding: 4px;
            list-style: none;
            }
    """
    def __init__(self, session_key="flash"):
        self.session_key = session_key

    def __call__(self, message):
        from pylons import session
        session.setdefault(self.session_key, []).append(message)
        session.save()

    def pop_messages(self):
        from pylons import session
        messages = session.pop(self.session_key, [])
        session.save()
        return messages


class Counter(object):
    """I count the number of occurrences of each value registered with me.
    
    Usage:
    >>> counter = Counter()
    >>> counter("foo")
    >>> counter("bar")
    >>> counter("foo")
    >>> sorted(counter.result.items())
    [('bar', 1), ('foo', 2)]

    >> counter.result
    {'foo': 2, 'bar': 1}

    To see the most frequently-occurring items in order:

    >>> counter.get_popular(1)
    [(2, 'foo')]
    >>> counter.get_popular()
    [(2, 'foo'), (1, 'bar')]

    Or if you prefer the list in item order:

    >>> counter.get_sorted_items()
    [('bar', 1), ('foo', 2)]
    """

    def __init__(self):
        self.result = defaultdict(int)
        self.total = 0  # Number of times instance has been called.

    def __call__(self, item):
        """Register an item with the counter."""
        self.result[item] += 1
        self.total += 1

    def get_popular(self, max_items=None):
        """Return the results as as a list of (count, item) pairs, with the
        most frequently occurring items first.
        If ``max_items`` is provided, return no more than that many items.
        """
        data = [(x[1], x[0]) for x in self.result.iteritems()]
        data.sort(key=lambda x: (sys.maxint - x[0], x[1]))
        if max_items:
            return data[:max_items]
        else:
            return data

    def get_sorted_items(self):
        """Return the result as a list of (item, count) pairs sorted by item.
        """
        data = self.result.items()
        data.sort()
        return data

class Accumulator(object):
    """Accumulate a dict of all values for each key.

    Usage:
    >>> bowling_scores = Accumulator()
    >>> bowling_scores("Fred", 0)
    >>> bowling_scores("Barney", 10)
    >>> bowling_scores("Fred", 1)
    >>> bowling_scores("Barney", 9)
    >>> sorted(bowling_scores.result.items())
    [('Barney', [10, 9]), ('Fred', [0, 1])]

    >> bowling_scores.result
    {'Fred': [0, 1], 'Barney': [10, 9]}

    The values are stored in the order they're registered.

    Alternatives to this class include ``paste.util. multidict.MultiDict``
    in Ian Bicking's Paste package.
    """

    def __init__(self):
        self.result = defaultdict(list)

    def __call__(self, key, value):
        self.result[key].append(value)


class UniqueAccumulator(object):
    """Accumulate a dict of unique values for each key.

    The values are stored in an unordered set.
    """

    def __init__(self):
        self.result = defaultdict(set)

    def __call__(self, key, value):
        self.result[key].add(value)


def unique(it):
    """Return a list of unique elements in the iterable, preserving the order.

    Usage:
    >>> unique([None, "spam", 2, "spam", "A", "spam", "spam", "eggs", "spam"])
    [None, 'spam', 2, 'A', 'eggs']
    """
    seen = set()
    ret = []
    for elm in it:
        if elm not in seen:
            ret.append(elm)
            seen.add(elm)
    return ret

def only_some_keys(dic, *keys):
    """Return a copy of the dict with only the specified keys present.  
    
    ``dic`` may be any mapping; the return value is always a Python dict.
    """
    ret = {}
    for key in keys:
        ret[key] = dic[key]   # Raises KeyError.
    return ret

def except_keys(dic, *keys):
    """Return a copy of the dict without the specified keys.
    """
    ret = dic.copy()
    for key in keys:
        try:
            del ret[key]
        except KeyError:
            pass
    return ret

def extract_keys(dic, *keys):
    """Return two copies of the dict.  The first has only the keys
       specified.  The second has all the *other* keys from the original dict.
    """
    for k in keys:
        if k not in dic:
            raise KeyError("key %r is not in original mapping" % k)
    r1 = {}
    r2 = {}
    for k, v in dic.items():
        if k in keys:
            r1[k] = v
        else:
            r2[k] = v
    return r1, r2

def ordered_items(dic, key_order, other_keys=True, default=NoDefault):
    """Like dict.iteritems() but with a specified key order.

    ``dic`` is any mapping.
    ``key_order`` is a list of keys.  Items will be yielded in this order.
    ``other_keys`` is a boolean.
    ``default`` is a value returned if the key is not in the dict.

    This yields the items listed in ``key_order``.  If a key does not exist
    in the dict, yield the default value if specified, otherwise skip the
    missing key.  Afterwards, if ``other_keys`` is true, yield the remaining
    items in an arbitrary order.

    Usage:
    >>> dic = {"To": "you", "From": "me", "Date": "2008/1/4", "Subject": "X"}
    >>> dic["received"] = "..."
    >>> order = ["From", "To", "Subject"]
    >>> list(ordered_items(dic, order, False))
    [('From', 'me'), ('To', 'you'), ('Subject', 'X')]
    """
    d = dict(dic)
    for key in key_order:
        if key in d:
            yield key, d.pop(key)
        elif default is not NoDefault:
            yield key, default
    if other_keys:
        for key, value in d.iteritems():
            yield key, value

def del_quiet(dic, *keys):
    """Delete several keys from a dict, ignoring those that don't exist.
    
    This modifies the dict in place.
    """
    for key in keys:
        try:
            del dic[key]
        except KeyError:
            pass

def dict_of_dicts(dicts, key):
    """Correlate several dicts under one superdict.

    E.g., If you have several dicts each with a 'name' key, this will
    create a superdict containing each dict keyed by name.
    """
    ret = {}
    i = 0
    for d in dicts:
        try:
            my_key = d[key]
        except KeyError:
            msg = "'dicts' element %d contains no key '%s'"
            tup = i, key 
            raise KeyError(msg % tup)
        ret[my_key] = d
        i += 1
    return ret


def dict_of_objects(objects, attr):
    """Correlate several dict under one dict.

    E.g., If you have several objects each with a 'name' attribute, this will
    create a dict containing each object keyed by name.
    """
    ret = {}
    i = 0
    for obj in objects:
        try:
            my_key = getattr(obj, attr)
        except AttrError:
            msg = "'%s' object at 'objects[%d]' contains no attribute '%s'"
            tup = type(obj).__name__, i, attr 
            raise AttributeError(msg % tup)
        ret[my_key] = obj
        i += 1
    return ret


def distribute(lis, columns, horizontal=False, fill=None):
    """Distribute a list into a N-column table (list of lists).

    Each list in the return value represents one row of the table.
    table[0] is the first row.
    table[0][1] is the first column in the first row.
    
    If ``horizontal`` is true, the elements are distributed horizontally,
    filling each row before going on to the next.  Use this if you're building
    an HTML table.  If the data runs out before the last row is completed,
    the remaining cells are filled with the ``fill`` value to ensure all rows
    are equal length.
    
    If false (default), the elements are distributed vertically, filling all
    table[N][0] elements before going to table[N][1].  The column length is
    calculated to ensure the smallest number of extra cells in the last
    column.  Extra cells are filled with the ``fill`` value.  This structure
    is useful to produce a list of words that can be output left to right but
    is alphabetical vertically like a dictionary or file listing.  It's also
    useful for HTML tables when an entire "column" will be placed in a single
    <td>, perhaps with a <br> or <li> between elements.
    """
    if columns < 1:
        raise ValueError("arg 'columns' must be >= 1")
    if horizontal:
        ret = []
        for i in range(0, len(lis), columns):
            row = lis[i:i+columns]
            row_len = len(row)
            if row_len < columns:
                extra = [fill] * (columns - row_len)
                row.extend(extra)
            ret.append(row)
        return ret
    lis_len = len(lis)
    column_len, remainder = divmod(lis_len, columns)
    if remainder:
        column_len += 1
    ret = [None] * columns
    for i in range(columns):
        start = i * column_len
        end = min(start + column_len, lis_len)
        #print "i=%d, start=%d, end=%d, element=%r" % (i, start, end, lis[start:end])
        ret[i] = lis[start:end]
    return ret


if __name__ == "__main__":
    import doctest
    doctest.testmod()
