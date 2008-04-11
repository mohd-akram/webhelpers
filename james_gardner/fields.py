from webhelpers import options_for_select, start_form

def form_start(*k, **p):
    form = ''
    if k or p:
        form = start_form(*k, **p)
    return '<table class="%s">%s'%(
        p.get('table_class', 'form'),
        form,
    )

def form_end():
    return '</table>'

def field(label='', field='', required=False, field_desc='', label_desc='', sub_label='', help='', defect='', error=''):

    field = error+field
    if label:
        label = label + ':'
    output = []
    if required:
        required = '<span class="required">*</span> '
    else:
        required = ''
    desc = ''
    if sub_label:
        desc = '<br /><span class="small">%s</span>'%sub_label
    if help and defect:
        output.append('<tr class="field"><td valign="top" class="label">'+required+'<label>'+label+'</label>'+desc+'</td><td>'+field+'</td><td>'+help+'</td><td>'+defect+'</td></tr>')
    elif help or defect:
        html=help or defect 
        output.append('<tr class="field"><td valign="top" class="label">'+required+'<label>'+label+'</label>'+desc+'</td><td>'+field+'</td><td colspan="2">'+html+'</td></tr>')
    else:
        output.append('<tr class="field"><td valign="top" class="label">'+required+'<label>'+label+'</label>'+desc+'</td><td colspan="3">'+field+'</td></tr>')
    if label_desc or field_desc:
        output.append('<tr class="description"><td valign="top" class="label"><span class="small">'+label_desc+'</span></td><td valign="top" colspan="3"><span class="small">'+field_desc+'</span></td></tr>')
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

