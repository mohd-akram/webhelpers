"""
Form Tag Helpers
"""

from html import HTML, escape, lit_sub

def form(url, method="POST", multipart=False, **options):
    """
    Start a form tag that points the action to an url. 
    
    The url options should be given either as a string, or as a ``url()``
    function. The method for the form defaults to POST.
    
    Options:

    ``multipart``
        If set to True, the enctype is set to "multipart/form-data".
    ``method``
        The method to use when submitting the form, usually either "GET" or 
        "POST". If "PUT", "DELETE", or another verb is used, a hidden input
        with name _method is added to simulate the verb over POST.
    """
    if multipart:
        options["enctype"] = "multipart/form-data"
    
    method_tag = HTML.literal("")

    if method.upper() in ['POST', 'GET']:
        options['method'] = method
    else:
        options['method'] = "POST"
        method_tag = HTML.input(
            type="hidden", id="_method", name_="_method", value=method)
    
    options["action"] = url
    options["_closed"] = False
    return HTML.form(method_tag, **options)

def end_form():
    """
    Output "</form>".
    
    Example::

        >>> end_form()
        literal(u'</form>')
    """
    return HTML.literal("</form>")

def text(name, value=None, **options):
    """
    Create a standard text field.
    
    ``value`` is a string, the content of the text field.
    
    Options:
    
    * ``disabled`` - If set to True, the user will not be able to use 
        this input.
    * ``size`` - The number of visible characters that will fit in the 
        input.
    * ``maxlength`` - The maximum number of characters that the browser 
        will allow the user to enter.
    
    Remaining keyword options will be standard HTML options for the tag.
    
    """
    o = {'type': 'text', 'name_': name, 'id': name, 'value': value}
    o.update(options)
    return HTML.input(**o)

def hidden(name, value=None, **options):
    """
    Create a hidden field.
    
    Takes the same options as text_field.
    
    """
    options.update(dict(type="hidden", name=name, value=value))
    return HTML.input(**options)

def file(name, value=None, **options):
    """
    Create a file upload field.
    
    If you are using file uploads then you will also need to set the 
    multipart option for the form.

    Example::

        >>> file('myfile')
        literal(u'<input id="myfile" name="myfile" type="file" />')
        
    """
    options.update(dict(type="file", id=options.get('id', name), name=name, value=value))
    return HTML.input(**options)

def password(name="password", value=None, **options):
    """
    Create a password field.
    
    Takes the same options as text_field.
    
    """
    options.update(dict(type="password", id=options.get('id', name), name=name, value=value))
    return HTML.input(**options)

def textarea(name, content='', **options):
    """
    Create a text input area.
    
    Options:
    
    * ``size`` - A string specifying the dimensions of the textarea.
    
    Example::
    
        >>> textarea("body", '', size="25x10")
        literal(u'<textarea cols="25" id="body" name="body" rows="10"></textarea>')
        
    """
    if 'size' in options:
        options["cols"], options["rows"] = options["size"].split("x")
        del options['size']
    o = {'name_': name, 'id': name}
    o.update(options)
    return HTML.textarea(content, **o)

def checkbox(name, value="1", checked=False, **options):
    """
    Create a check box.

    Example::
    
        >>> checkbox("hi")
        literal(u'<input id="hi" name="hi" type="checkbox" value="1" />')
    """
    o = {'type': 'checkbox', 'name_': name, 'id': name, 'value': value}
    o.update(options)
    if checked:
        o["checked"] = "checked"
    return HTML.input(**o)

def radiobutton(name, value, checked=False, **options):
    """Create a radio button.
    
    The id of the radio button will be set to the name + ' ' + value to 
    ensure its uniqueness.
    
    """
    pretty_tag_value = re.sub(r'\s', "_", '%s' % value)
    pretty_tag_value = re.sub(r'(?!-)\W', "", pretty_tag_value).lower()
    html_options = {'type': 'radio', 'name': name, 'id': '%s_%s' % (name, pretty_tag_value), 'value': value}
    html_options.update(options)
    if checked:
        html_options["checked"] = "checked"
    return HTML.input(**html_options)

def submit(value="Save changes", name='commit', confirm=None, disable_with=None, **options):
    """Create a submit button with the text ``value`` as the caption.

    Options:

    * ``confirm`` - A confirm message displayed when the button is clicked.
    * ``disable_with`` - The value to be used to rename a disabled version 
      of the submit button.
      
    """
    if confirm:
        onclick = options.get('onclick', '')
        if onclick.strip() and not onclick.rstrip().endswith(';'):
            onclick += ';'
        options['onclick'] = "%sreturn %s;" % (onclick, confirm_javascript_function(confirm))

    if disable_with:
        options["onclick"] = "this.disabled=true;this.value='%s';this.form.submit();%s" % (disable_with, options.get("onclick", ''))
    o = {'type': 'submit', 'name': name, 'value': value }
    o.update(options)
    return HTML.input(**o)

__all__ = ['form', 'end_form', 'select', 'text', 'hidden', 'file',
           'password', 'text', 'checkbox', 'radiobutton', 'submit']
