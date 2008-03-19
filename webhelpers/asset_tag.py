"""
Asset Tag Helpers

Provides functionality for linking an HTML page together with other 
assets, such as images, javascripts, stylesheets, and feeds.

"""
import os
import urlparse
from html import HTML
from routes import request_config

# The absolute path of the WebHelpers javascripts directory
javascript_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'javascripts')

def auto_discovery_link(source, feed_type='rss', **kwargs):
    """
    Return a link tag allowing auto-detecting of RSS or ATOM feed.
    
    The auto-detection of feed for the current page is only for browsers
    and news readers that support it.

    ``source``
        The URL of the feed. The URL is ultimately prepended with the 
        environment's ``SCRIPT_NAME`` (the root path of the web 
        application), unless the URL is fully-fledged 
        (e.g. http://example.com).

    ``feed_type``
        The type of feed. Specifying 'rss' or 'atom' automatically 
        translates to a type of 'application/rss+xml' or 
        'application/atom+xml', respectively. Otherwise the type is used 
        as specified. Defaults to 'rss'.
        
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
    kwargs.pop('href', None)
    kwargs.pop('type', None)
    tag_args.update(kwargs)
    return HTML.link(**tag_args)

def image(source, alt=None, height=None, width=None, **options):
    """
    Return an image tag for the specified ``source``.

    ``source``
        The source URL of the image. The URL is prepended with '/images/', 
        unless its full path is specified. The URL is ultimately 
        prepended with the environment's ``SCRIPT_NAME`` (the root path 
        of the web application), unless the URL is fully-fledged (e.g. 
        http://example.com).
    
    ``alt``
        The img's alt tag. Defaults to the source's filename, title cased.

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
    options['src'] = compute_public_path(source, 'images')

    if not alt:
        alt = os.path.splitext(os.path.basename(source))[0].title()
    options['alt'] = alt
    
    if width is not None:
        options['width'] = width
    if height is not None:
        options['height'] = height
        
    return HTML.img(**options)

def javascript_link(*sources, **options):
    """
    Return script include tags for the specified javascript ``sources``.
    
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
    if options.get('defer') == True:
        options['defer'] = 'defer'

    tags = []
    for source in sources:
        content_options = dict(type='text/javascript',
                src=compute_public_path(source, 'javascripts', 'js'))
        content_options.update(options)
        tags.append(HTML.script('',  **content_options))
    return '\n'.join(tags)

def stylesheet_link(*sources, **options):
    """
    Return CSS link tags for the specified stylesheet ``sources``.

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
    tag_options = dict(rel='Stylesheet', type='text/css', media='screen')
    tag_options.update(options)
    tag_options.pop('href', None)

    tags = [HTML.link(**dict(href=compute_public_path(source, 
                                                      'stylesheets', 
                                                      'css'),
                               **tag_options)) for source in sources]
    return '\n'.join(tags)
    
def compute_public_path(source, root_path=None, ext=None):
    """
    Format the specified source for publishing.
    
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

def get_script_name():
    """
    Determine the current web application's ``SCRIPT_NAME``.
    """
    script_name = ''
    config = request_config()
    if hasattr(config, 'environ'):
        script_name = config.environ.get('SCRIPT_NAME', '')
    return script_name

__all__ = ['javascript_path', 'auto_discovery_link',
           'image', 'javascript_link', 'stylesheet_link']
