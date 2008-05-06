"""\
Functions to help in the formatting of forms
"""

from webhelpers.tags import form as start_form, end_form
from webhelpers.html import HTML, literal
from webhelpers.rails import options_for_select

def form_start(*k, **p):
    """\
    Start a form the way you would with ``start_form()`` but include the HTML
    necessary for the use of the ``fields()`` helper. 
    
    >>> form_start('/action', method='post')
    literal(u'<table><form action="/action" method="post">')
    >>> form_start('/action', method='post', table_class='form')
    literal(u'<table class="form"><form action="/action" method="post">')
    """
    if p.has_key('table_class'):
         table_class = p.get('table_class', 'form')
         del p['table_class']
         return HTML.table(
             _closed=False, 
             class_=p.get('table_class', 'form'),
             c=start_form(*k,**p)
         )
    else:
         return HTML.table(_closed=False, c=start_form(*k,**p))

def form_end(*k, **p):
    """\
    End a form started with ``form_start()``
    >>> form_end()
    literal(u'</form></table>')
    """
    return end_form(*k, **p)+literal("</table>")

def field(
    label='', 
    field='', 
    required=False, 
    label_desc='', 
    field_desc='',
    sub_label='', 
    help='',
    error=''
):
    """\
    Format a field with a label. 

    ``label``
        The label for the field

    ``field``
        The HTML representing the field, wrapped in ``literal()``

    ``required``
         Can be ``True`` or ``False`` depending on whether the label should be 
         formatted as required or not. By default required fields have an
         asterix.

    ``label_desc``
        Any text to appear underneath the label, level with ``field_desc`` 

    ``field_desc``
        Any text to appear underneath the field

    ``sub_label``
        Any text to appear immediately beneath the label but above the 
        label_desc. This is useful if the field itself is very large and using
        label_desc would result in the description of the label being a long 
        way from the label itself.

    ``help``
        Any HTML or JavaScript to appear imediately to the right of the field 
        which could be used to implement a help system on the form

    ``error``
        Any text to appear immediately before the HTML field, usually used for
        an error message.

    It should be noted that when used with FormEncode's ``htmlfill`` module, 
    errors appear immediately before the HTML field in the position of the
    ``error`` argument. No ``<form:error>`` tags are added automatically by
    this helper because errors are placed there anyway and adding the tags
    would lead to this helper generating invalid HTML.
    """
    field = error+field
    if label:
        label = label + literal(':')
    output = []
    if required:
        required = HTML.span(class_="required", c='*')
    else:
        required = ''
    desc = ''
    if sub_label:
        desc = '<br /><span class="small">%s</span>'%sub_label
    if help:
        output.append(literal('<tr class="field"><td valign="top" class="label">')+required+HTML.label(c=label)+desc+literal('</td><td>')+field+literal('</td><td>')+help+literal('</td></tr>'))
    else:
        output.append(literal('<tr class="field"><td valign="top" class="label">')+required+HTML.label(c=label)+desc+literal('</td><td colspan="2">')+field+literal('</td></tr>'))
    if label_desc or field_desc:
        output.append(literal('<tr class="description"><td valign="top" class="label"><span class="small">')+label_desc+literal('</span></td><td valign="top" colspan="2"><span class="small">')+field_desc+literal('</span></td></tr>'))
    return ''.join(output)



def options_with_caption(container, caption='Please select...', pos=0, value='', *k, **p):
    """\
    Return a some select options adding in a value of '' with a caption specified by ``text``.
    """
    if pos=='end':
        container.append([caption, value])
    else:
        container.insert(pos, [caption, value])
    return options_for_select(container, *k, **p)

def ids_from_options(options):
    """\
    Return the IDs of all the options used to create a select box. Useful when using
    a ``OneOf`` formencode validator.
    """
    return [str(x[1]) for x in options]

def value_from_option_id(options, id):
    """\
    Attempts to return a value for the option specified, returns ``""``
    if the option specified is ``None`` so that it works with the 
    ``options_with_please_select()`` helper above. 
    """
    if not id:
        return ''
    if isinstance(options, (list, tuple)):
        if len(options) and isinstance(options[0], (list, tuple)):
            for v, k in options:
                if unicode(k) == unicode(id):
                    return v
        else:
            # Assume it is a list where the ids are the values:
            if unicode(id) in [unicode(x) for x in options]:
                return id
    raise Exception("Option %s not found or invalid option format"%id)
    
def radio_group(name, options, value=None, align='horiz', cols=4):
    """Radio Group Field."""
    output=''
    if len(options)>0:
        if align <> 'table':
            for option in options:
                checked=''
                if not isinstance(option, list) and not isinstance(option, tuple):
                    k = option
                    v = option
                else:
                    k, v = option
                if unicode(v) == unicode(value):
                    checked=" checked"
                break_ = ''
                if align == 'vert':
                    break_='<br />'
                output+='<input type="radio" name="%s" value="%s"%s /> %s%s\n'%(name, v, checked, k, break_)
        else:
            output += '<table border="0" width="100%" cellpadding="0" cellspacing="0">\n    <tr>\n'
            counter = -1
            for option in options:
                counter += 1
                if ((counter % cols) == 0) and (counter <> 0):
                    output += '    </tr>\n    <tr>\n'
                output += '      <td>'
                checked=''
                align=''
                if not isinstance(option, list) and not isinstance(option, tuple):
                    k = option
                    v = option
                else:
                    k=option[0]
                    v=option[1]
                if unicode(v)==unicode(value):
                    checked=" checked"
                output += '<input type="radio" name="%s" value="%s"%s /> %s%s'%(name, v, checked, k,align)
                output += '</td>\n      <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n'
            counter += 1
            while (counter % cols):
                counter += 1
                output += '      <td></td>\n      <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n'
            output += '    </tr>\n</table>'
    return output

def _format_values(values):
    if not isinstance(values, list) and not isinstance(values, tuple):
        return [unicode(values)]
    else:
        values_ = []
        for value in values:
            values_.append(unicode(value))
        return values_

def checkbox_group(name, options, values=None, align='horiz', cols=4):
    """Check Box Group Field."""
    values = _format_values(values)
    output = u''
    item_counter = 0
    if len(options) > 0:
        if align <> 'table':
            for option in options:
                if not isinstance(option, list) and not isinstance(option, tuple):
                    k = option
                    v = option
                else:
                    k=option[0]
                    v=option[1]
                checked=u''
                if unicode(v) in values:
                    checked=" checked"
                break_ = u''
                if align == 'vert':
                    break_=u'<br />'
                output+='<input type="checkbox" name="%s" value="%s"%s /> %s%s\n'%(name, v, checked, k, break_)
                item_counter += 1
        else:
            output += u'<table border="0" width="100%" cellpadding="0" cellspacing="0">\n    <tr>\n'
            counter = -1
            for option in options:
                counter += 1
                if ((counter % cols) == 0) and (counter <> 0):
                    output += u'    </tr>\n    <tr>\n'
                output += '      <td>'
                checked=u''
                align=u''
                if not isinstance(option, list) and not isinstance(option, tuple):
                    k = option
                    v = option
                else:
                    k=option[0]
                    v=option[1]
                if unicode(v) in values:
                    checked=" checked"
                output += u'<input type="checkbox" name="%s" value="%s"%s />%s%s'%(name, v, checked, k, align)
                item_counter += 1
                output += u'</td>\n      <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n'
            counter += 1
            while (counter % cols):
                counter += 1
                output += u'      <td></td>\n      <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>\n'
            output += u'    </tr>\n</table>\n'
    if not type(output) == unicode:
        raise Exception(type(output))
    return output[:-1]

if __name__ == '__main__':
    import doctest
    doctest.testmod()

