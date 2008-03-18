"""
Form and Form Options Helpers
"""

import html

def options_for_select(container, selected=None, function=None):
    """
    Create select options from a container (list, tuple, dict), or
    objects/dicts in a container.
    
    Accepts a container (list, tuple, dict) and returns a string of 
    option tags. Given a container where the elements respond to first 
    and last (such as a two-element array), the "lasts" serve as option 
    values and the "firsts" as option text. Dicts are turned into this 
    form automatically, so the keys become "firsts" and values become 
    lasts. If ``selected`` is specified, the matching "last" or element 
    will get the selected option-tag. ``Selected`` may also be an array 
    of values to be selected when using a multiple select.
    
    If the container has dicts or objects, it will use the ``function``
    which must be specified and applies this function to each object or
    dictionary in the container.  This function should return a tuple of
    the option text and value of the dict or object.
    
    Examples (call, result)::
    
        >>> options_for_select([["Dollar", "$"], ["Kroner", "DKK"]])
        '<option value="$">Dollar</option>\\n<option value="DKK">Kroner</option>'
        >>> options_for_select([ "VISA", "MasterCard" ], "MasterCard")
        '<option value="VISA">VISA</option>\\n<option selected="selected" value="MasterCard">MasterCard</option>'
        >>> options_for_select(dict(Basic="$20", Plus="$40"), "$40")
        '<option selected="selected" value="$40">Plus</option>\\n<option value="$20">Basic</option>'
        >>> options_for_select([ "VISA", "MasterCard", "Discover" ], ["VISA", "Discover"])
        '<option selected="selected" value="VISA">VISA</option>\\n<option value="MasterCard">MasterCard</option>\\n<option selected="selected" value="Discover">Discover</option>'
        >>> def make_elem(x):
        ...     return x.name, x.price
        ...
        >>> class myObj(object):
        ...     name = ""
        ...     price = ""
        ...
        >>> myObj1 = myObj()
        >>> myObj1.name = "Basic"
        >>> myObj1.price = "$20"
        >>> myObj2 = myObj()
        >>> myObj2.name = "Plus"
        >>> myObj2.price = "$40"
        >>> options_for_select([myObj1, myObj2], selected="$40", function=make_elem)
        '<option value="$20">Basic</option>\\n<option selected="selected" value="$40">Plus</option>'
        >>> def make_elem(x):
        ...     return x["name"], x["price"]
        >>> options_for_select([{"name":"Basic", "price":"$20"},{"name":"Plus","price":"$40"}], selected="$40", function=make_elem)
        '<option value="$20">Basic</option>\\n<option selected="selected" value="$40">Plus</option>'
        
    Note: Only the option tags are returned.  You have to wrap this call 
    in a regular HTML select tag.
    
    """
    options = []
    if (not container):
        return ''
    
    if (not isinstance(selected, (list, tuple))):
        selected = (selected, )

    if (hasattr(container, 'values')):
        container = container.items()

    elif (isinstance(container[0], (dict, object))):
        if (function):
            container = [function(x) for x in container]

    if (not isinstance(container[0], (list, tuple))):
        container = [(x, x) for x in container]
        
    for x in container:
        if (x[1] in selected):
            options.append(str(html.HTML.option(x[0], value=x[1], selected="selected")))
        else:
            options.append(str(html.HTML.option(x[0], value=x[1])))
            
    return "\n".join(options)
    
__all__ = ['options_for_select']
