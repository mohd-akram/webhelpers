"""Helpers producing simple HTML tags"""

import os
import re
import urllib
import urlparse

try:
    from routes import request_config
except ImportError:
    request_config = None

from webhelpers.html import escape, HTML, literal, url_escape

__all__ = [
           # Form tags
           "form", 
           "end_form", 
           "text", 
           "textarea", 
           "hidden", 
           "file",
           "password", 
           "text", 
           "checkbox", 
           "radio", 
           "submit",
           "select", 
           "ModelTags",
           # hyperlinks
           "link_to",
           "link_to_if",
           "link_to_unless",
           # Other tags
           "image",
           # Head tags
           "auto_discovery_link",
           "javascript_link",
           "javascript_path",
           "stylesheet_link",
           # Utility functions
           "convert_boolean_attrs",
           ]


def form(url, method="POST", multipart=False, **attrs):
    """Start a form tag that points the action to an url.
    
    The url options should be given either as a string, or as a 
    ``url()`` function. The method for the form defaults to POST.
    
    Options:

    ``multipart``
        If set to True, the enctype is set to "multipart/form-data".
    ``method``
        The method to use when submitting the form, usually either 
        "GET" or "POST". If "PUT", "DELETE", or another verb is used, a
        hidden input with name _method is added to simulate the verb
        over POST.
    
    """
    if multipart:
        attrs["enctype"] = "multipart/form-data"
    method_tag = literal("")
    if method.upper() in ['POST', 'GET']:
        attrs['method'] = method
    else:
        attrs['method'] = "POST"
        method_tag = HTML.input(type="hidden", name="_method", value=method)
    attrs["action"] = url
    return HTML.form(method_tag, _closed=False, **attrs)


def end_form():
    """Output "</form>".
    
    Example::

        >>> end_form()
        literal(u'</form>')
    
    """
    return literal("</form>")


def text(name, value=None, **attrs):
    """Create a standard text field.
    
    ``value`` is a string, the content of the text field.
    
    Options:
    
    * ``disabled`` - If set to True, the user will not be able to use
        this input.
    * ``size`` - The number of visible characters that will fit in the
        input.
    * ``maxlength`` - The maximum number of characters that the browser
        will allow the user to enter.
    
    The remaining keyword args will be standard HTML attributes for the tag.
    
    """
    set_input_attrs(attrs, "text", name, value)
    convert_boolean_attrs(attrs, ["disabled"])
    return HTML.input(**attrs)


def hidden(name, value=None, **attrs):
    """Create a hidden field.
    """
    set_input_attrs(attrs, "hidden", name, value)
    return HTML.input(**attrs)


def file(name, value=None, **attrs):
    """Create a file upload field.
    
    If you are using file uploads then you will also need to set the 
    multipart option for the form.

    Example::

        >>> file('myfile')
        literal(u'<input name="myfile" type="file" />')
    
    """
    set_input_attrs(attrs, "file", name, value)
    return HTML.input(**attrs)


def password(name="password", value=None, **attrs):
    """Create a password field.
    
    Takes the same options as text_field.
    
    """
    set_input_attrs(attrs, "password", name, value)
    return HTML.input(**attrs)


def textarea(name, content='', **attrs):
    """Create a text input area.
    
    Example::
    
        >>> textarea("body", '', cols=25, rows=10)
        literal(u'<textarea cols="25" name="body" rows="10"></textarea>')
    
    """
    attrs["name"] = name
    return HTML.textarea(content, **attrs)


def checkbox(name, value="1", checked=False, **attrs):
    """Create a check box.

    Options:

    * ``checked`` - If true, the checkbox will be initially checked.
      This may be specified as a positional argument.

    * ``disabled`` - If true, checkbox will be grayed out.

    * ``readonly`` - If true, the user will not be able to modify the checkbox.

    Example::
    
        >>> checkbox("hi")
        literal(u'<input name="hi" type="checkbox" value="1" />')
    
    """
    set_input_attrs(attrs, "checkbox", name, value)
    attrs["type"] = "checkbox"
    attrs["name"] = name
    attrs["value"] = value
    if checked:
        attrs["checked"] = "checked"
    convert_boolean_attrs(attrs, ["disabled", "readonly"])
    return HTML.input(**attrs)


def radio(name, value, checked=False, **attrs):
    """Create a radio button.
    
    The id of the radio button will be set to the name + ' ' + value to 
    ensure its uniqueness.  An ``id`` keyword arg overrides this.
    
    """
    set_input_attrs(attrs, "radio", name, value)
    if checked:
        attrs["checked"] = "checked"
    if not "id" in attrs:
        pretty_tag_value = re.sub(r'\s', "_", '%s' % value)
        pretty_tag_value = re.sub(r'(?!-)\W', "", pretty_tag_value).lower()
        attrs["id"] = '%s_%s' % (name, pretty_tag_value)
    return HTML.input(**attrs)


def submit(value="Save changes", name='commit', **attrs):
    """Create a submit button with the text ``value`` as the caption."""
    set_input_attrs(attrs, "submit", name, value)
    return HTML.input(**attrs)


def select(name, selected_values, options, **attrs):
    """Create a dropdown selection box.

    * ``name`` -- the name of this control.

    * ``selected_values`` -- a string or list of strings giving the
      value(s) that should be preselected.

    * ``options`` -- an iterable of ``(label, value)`` pairs.  The label
      is what's shown to the user; the value is what's seen by the 
      application if the user chooses this option.  Hint: you can use
      ``sorted(options)`` to display the labels alphabetically.  You can
      also pass an iterable of strings, in which case the labels and values
      will be identical.

    * ``multiselect`` -- if true, this control will allow multiple
       selections.

    Any other keyword args will become HTML attributes for the <select>.

    Examples (call, result)::
    
        >>> select("currency", "$", [["Dollar", "$"], ["Kroner", "DKK"]])
        literal(u'<select name="currency">\\n<option selected="selected" value="$">Dollar</option>\\n<option value="DKK">Kroner</option>\\n</select>')
        >>> select("cc", "MasterCard", [ "VISA", "MasterCard" ], id="cc", class_="blue")
        literal(u'<select class="blue" id="cc" name="cc">\\n<option value="VISA">VISA</option>\\n<option selected="selected" value="MasterCard">MasterCard</option>\\n</select>')
        >>> select("cc", ["VISA", "Discover"], [ "VISA", "MasterCard", "Discover" ])
        literal(u'<select name="cc">\\n<option selected="selected" value="VISA">VISA</option>\\n<option value="MasterCard">MasterCard</option>\\n<option selected="selected" value="Discover">Discover</option>\\n</select>')
        
    """
    attrs["name"] = name
    convert_boolean_attrs(attrs, ["multiple"])
    if isinstance(selected_values, basestring):
        selected_values = (selected_values,)
    opts = []
    for x in options:
        if isinstance(x, basestring):
            label = value = x
        else:
            label = x[0]
            value = x[1]
        if value in selected_values:
            opt = HTML.option(label, value=value, selected="selected")
        else:
            opt = HTML.option(label, value=value)
        opts.append(opt)
    opts_html = "\n".join(opts)
    opts_html = literal("\n%s\n" % opts_html)
    return HTML.select(opts_html, **attrs)


class ModelTags(object):
    """A nice way to build a form from a database record.
    
    ModelTags allows you to build a create/update form easily.  (This is the
    C and U in CRUD.)  The constructor takes a database record, which can be
    a SQLAlchemy mapped class, or any object with attributes or keys for the
    field values.  Its methods shadow the the form field helpers, but it
    automatically fills in the value attributes based on the current value in
    the record.

    You can also use the same form for to input a new record.  Pass `None` or
    `""` instead of a record, and it will set all the current values to a
    default value, which is either the `default` keyword arg to the method, or
    `""` if not specified.
    """

    undefined_values = set([None, ""])

    def __init__(self, record, use_keys=False):
        self.record = record
        self.use_keys = use_keys
    
    def checkbox(self, name, **kw):
        value = kw.pop("value", "1")
        checked = bool(self._get_value(name))
        return checkbox(name, value, checked, **kw)

    def file(self, name, **kw):
        value = self._get_value(name, kw)
        return file(name, value, **kw)

    def hidden(self, name, **kw):
        value = self._get_value(name, kw)
        return hidden(name, value, **kw)

    def password(self, name, **kw):
        value = self._get_value(name, kw)
        return password(name, value, kw)

    def radio(self, name, checked_value, **kw):
        value = self._get_value(name, kw)
        checked = (value == checked_value)
        return radio(name, value, checked, **kw)

    def select(self, name, options, **kw):
        selected_values = self._get_value(name, kw)
        return select(name, selected_values, options, **kw)

    def text(self, name, *args, **kw):
        value = self._get_value(name, kw)
        return text(name, value, **kw)

    def textarea(self, name, *args, **kw):
        content = self._get_value(name, kw)
        return textarea(name, content, **kw)

    # Private methods.
    def _get_value(self, name, kw):
        """Modifies `kw` in place!"""
        default = kw.pop("default", "")
        if self.record in self.undefined_values:
            return default
        elif self.use_keys:
            return self.record[name]    # Raises KeyError.
        else:
            return getattr(self.record, name)   # Raises AttributeError.


#### Hyperlink tags

def link_to(label, url='', **attrs):
    """Create a hyperlink with the given text pointing to the URL.
    
    If the label is ``None`` or empty, the URL will be used as the label.

    This function does not modify the URL in any way.  The label will be
    escaped if it contains HTML markup.  To prevent escaping, wrap the label
    in a ``webhelpers.html.literal()``.
    """
    attrs['href'] = url
    return HTML.a(label or url, **attrs)


def link_to_if(condition, label, url='', **attrs):
    """Same as ``link_to`` but return just the label if the condition is false.
    
    This is useful in a menu when you don't want the current option to be a
    link.
    """
    if condition:
        return link_to(label, url, **attrs)
    else:
        return label

def link_to_unless(condition, label, url='', **attrs):
    """Same as ``link_to`` but return just the label if the condition is true.
    """
    if not condition:
        return link_to(label, url, **attrs)
    else:
        return label



#### Non-form tags

def image(source, alt=None, height=None, width=None, **attrs):
    """Return an image tag for the specified ``source``.

    ``source``
        The source URL of the image. The URL is prepended with 
        '/images/', unless its full path is specified. The URL is
        ultimately prepended with the environment's ``SCRIPT_NAME``
        (the root path of the web application), unless the URL is 
        fully-fledged (e.g. http://example.com).
    
    ``alt``
        The img's alt tag. Defaults to the source's filename, title
        cased.

    ``height``
        The height of the image, default is not included
        
    ``width``
        The width of the image, default is not included
        
    Examples::

        >>> image('xml.png')
        literal(u'<img alt="Xml" src="/images/xml.png" />')

        >>> image('rss.png', 'rss syndication')
        literal(u'<img alt="rss syndication" src="/images/rss.png" />')

        >>> image("icon.png", height=16, width=10, alt="Edit Entry")
        literal(u'<img alt="Edit Entry" height="16" src="/images/icon.png" width="10" />')

        >>> image("/icons/icon.gif", width=16, height=16)
        literal(u'<img alt="Icon" height="16" src="/icons/icon.gif" width="16" />')

        >>> image("/icons/icon.gif", width=16)
        literal(u'<img alt="Icon" src="/icons/icon.gif" width="16" />')
        
    """
    attrs['src'] = compute_public_path(source, 'images')

    if not alt:
        alt = os.path.splitext(os.path.basename(source))[0].title()
    attrs['alt'] = alt
    
    if width is not None:
        attrs['width'] = width
    if height is not None:
        attrs['height'] = height
        
    return HTML.img(**attrs)

#### Tags for the HTML head

# The absolute path of the WebHelpers javascripts directory
javascript_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'javascripts')

def javascript_link(*sources, **attrs):
    """Return script include tags for the specified javascript
    ``sources``.
    
    Specify the keyword argument ``defer=True`` to enable the script 
    defer attribute.

    Examples::
    
        >>> print javascript_link('/javascripts/prototype.js', '/other-javascripts/util.js')
        <script src="/javascripts/prototype.js" type="text/javascript"></script>
        <script src="/other-javascripts/util.js" type="text/javascript"></script>

        >>> print javascript_link('/app.js', '/test/test.1.js')
        <script src="/app.js" type="text/javascript"></script>
        <script src="/test/test.1.js" type="text/javascript"></script>
        
    """
    convert_boolean_attrs(attrs, ["defer"])
    tags = []
    for source in sources:
        content_attrs = dict(type='text/javascript',
                src=compute_public_path(source, 'javascripts', 'js'))
        content_attrs.update(attrs)
        tags.append(HTML.script('',  **content_attrs))
    return '\n'.join(tags)


def stylesheet_link(*sources, **attrs):
    """Return CSS link tags for the specified stylesheet ``sources``.

    Each source's URL path is ultimately prepended with the 
    environment's ``SCRIPT_NAME`` (the root path of the web 
    application), unless the URL path is a full-fledged URL 
    (e.g., http://example.com).
    
    Examples::

        >>> stylesheet_link('style.css')
        u'<link href="/stylesheets/style.css" media="screen" rel="Stylesheet" type="text/css" />'

        >>> stylesheet_link('/stylesheets/dir/file.css', media='all')
        u'<link href="/stylesheets/dir/file.css" media="all" rel="Stylesheet" type="text/css" />'

    """
    tag_attrs = dict(rel='Stylesheet', type='text/css', media='screen')
    tag_attrs.update(attrs)
    tag_attrs.pop('href', None)
    
    tags = [HTML.link(
        **dict(href=compute_public_path(source, 'stylesheets', 'css'), 
               **tag_attrs)) for source in sources]
    return '\n'.join(tags)


def auto_discovery_link(source, feed_type='rss', **attrs):
    """Return a link tag allowing auto-detecting of RSS or ATOM feed.
    
    The auto-detection of feed for the current page is only for
    browsers and news readers that support it.

    ``source``
        The URL of the feed. The URL is ultimately prepended with the
        environment's ``SCRIPT_NAME`` (the root path of the web 
        application), unless the URL is fully-fledged 
        (e.g. http://example.com).

    ``feed_type``
        The type of feed. Specifying 'rss' or 'atom' automatically 
        translates to a type of 'application/rss+xml' or 
        'application/atom+xml', respectively. Otherwise the type is
        used as specified. Defaults to 'rss'.
        
    Examples::

        >>> auto_discovery_link('http://feed.com/feed.xml')
        literal(u'<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />')

        >>> auto_discovery_link('http://feed.com/feed.xml', feed_type='atom')
        literal(u'<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />')

        >>> auto_discovery_link('app.rss', feed_type='atom', title='atom feed')
        literal(u'<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />')

        >>> auto_discovery_link('/app.html', feed_type='text/html')
        literal(u'<link href="/app.html" rel="alternate" title="" type="text/html" />')
        
    """
    title = ''
    if feed_type.lower() in ('rss', 'atom'):
        title = feed_type.upper()
        feed_type = 'application/%s+xml' % feed_type.lower()

    tag_args = dict(rel='alternate', type=feed_type, title=title,
                    href=compute_public_path(source))
    attrs.pop('href', None)
    attrs.pop('type', None)
    tag_args.update(attrs)
    return HTML.link(**tag_args)



########## INTERNAL FUNCTIONS ##########

def compute_public_path(source, root_path=None, ext=None):
    """Format the specified source for publishing.
    
    Use the public directory, if applicable.
    
    """
    if ext and not os.path.splitext(os.path.basename(source))[1]:
        source = '%s.%s' % (source, ext)

    # Avoid munging fully-fledged URLs, including 'mailto:'
    parsed = urlparse.urlparse(source)
    if not (parsed[0] and (parsed[1] or parsed[2])):
        # Prefix apps deployed under any SCRIPT_NAME path
        if not root_path or source.startswith('/'):
            source = '%s%s' % (get_script_name(), source)
        else:
            source = '%s/%s/%s' % (get_script_name(), root_path, source)
    return source


def convert_boolean_attrs(attrs, bool_attrs):
    """Convert boolean values into proper HTML attributes.

    ``attrs`` is a dict of HTML attributes, which will be modified in
    place.

    ``bool_attrs`` is a list of attribute names.

    For every element in ``bool_attrs``, I look for a corresponding key in
    ``attrs``.  If its value is true, I change the value to match the key.
    For example, I convert ``selected=True`` into ``selected="selected"``.  If
    the value is false, I delete the key.
    
    """
    for a in bool_attrs:
        if attrs.has_key(a) and attrs[a]:
            attrs[a] = a
        elif attrs.has_key(a):
            del attrs[a]

def set_input_attrs(attrs, type, name, value):
    attrs["type"] = type
    attrs["name"] = name
    attrs["value"] = value


def get_script_name():
    """Determine the current web application's ``SCRIPT_NAME``.
    
    .. note::
        This requires Routes to function, and will not pick up the
        SCRIPT_NAME var without it in use.
    
    """
    script_name = ''
    if request_config:
        config = request_config()
        if hasattr(config, 'environ'):
            script_name = config.environ.get('SCRIPT_NAME', '')
    else:
        script_name = ''
    return script_name


