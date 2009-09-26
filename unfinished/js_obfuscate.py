# XXX TODO: Convert js_obfuscate() to use webhelpers.html .
# The other functions are just dependencies.

def js_obfuscate(data):
    """Obfuscate data in a Javascript tag.
    
    Example::
        
        >>> js_obfuscate("<input type='hidden' name='check' value='valid' />")
        '<script type="text/javascript">\\n//<![CDATA[\\neval(unescape(\\'%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%27%3c%69%6e%70%75%74%20%74%79%70%65%3d%27%68%69%64%64%65%6e%27%20%6e%61%6d%65%3d%27%63%68%65%63%6b%27%20%76%61%6c%75%65%3d%27%76%61%6c%69%64%27%20%2f%3e%27%29%3b\\'))\\n//]]>\\n</script>'
        
    """
    tmp = "document.write('%s');" % data
    string = ''.join(['%%%x' % ord(x) for x in tmp])
    return javascript_tag("eval(unescape('%s'))" % string)

def javascript_tag(content, **html_options):
    """
    Return a JavaScript tag with the ``content`` inside.
    
    Example::
    
        >>> javascript_tag("alert('All is good')")
        '<script type="text/javascript">\\n//<![CDATA[\\nalert(\\'All is good\\')\\n//]]>\\n</script>'
    """
    return content_tag("script", javascript_cdata_section(content), type="text/javascript",
                       **html_options)

def javascript_cdata_section(content):
    return "\n//%s\n" % cdata_section("\n%s\n//" % content)

def content_tag(name, content, **options):
    """
    Create a tag with content.
    
    Takes the same keyword args as ``tag``.
    
    Examples::
    
        >>> content_tag("p", "Hello world!")
        '<p>Hello world!</p>'
        >>> content_tag("div", content_tag("p", "Hello world!"), class_="strong")
        '<div class="strong"><p>Hello world!</p></div>'
        
    """
    if content is None:
        content = ''
    tag = '<%s%s>%s</%s>' % (name, (options and tag_options(**options)) or '', content, name)
    return tag

def cdata_section(content):
    """
    Return a CDATA section with the given ``content``.
    
    CDATA sections are used to escape blocks of text containing 
    characters which would otherwise be recognized as markup. CDATA 
    sections begin with the string ``<![CDATA[`` and end with (and may 
    not contain) the string ``]]>``. 
    
    """
    if content is None:
        content = ''
    return "<![CDATA[%s]]>" % content

def escape_once(html):
    """Escape a given string without affecting existing escaped entities.

    >>> escape_once("1 < 2 &amp; 3")
    '1 &lt; 2 &amp; 3'
    
    """
    return fix_double_escape(html_escape(html))

