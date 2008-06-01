"""Functions that convert from text markup languages to HTML.

"""

from webhelpers.html import literal
import webhelpers.textile as textile
import webhelpers.markdown as _markdown

__all__ = [
    'markdown', 
    'textilize',
    ]

def markdown(text, **kwargs):
    """Format the text with MarkDown formatting.
    
    This function uses the `Python MarkDown library 
    <http://www.freewisdom.org/projects/python-markdown/>`_
    which is included with WebHelpers.
    
    """
    return literal(_markdown.markdown(text, **kwargs))

def textilize(text, sanitize=False):
    """Format the text with Textile formatting.
    
    This function uses the `PyTextile library <http://dealmeida.net/>`_ 
    which is included with WebHelpers.
    
    Additionally, the output can be sanitized which will fix tags like 
    <img />,  <br /> and <hr /> for proper XHTML output.
    
    """
    texer = textile.Textiler(text)
    return literal(texer.process(sanitize=sanitize))
