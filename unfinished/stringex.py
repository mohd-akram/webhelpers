# coding: utf-8
"""A light port of some useful string functions from the Ruby package
stringex

http://github.com/rsl/stringex/tree/master

"""
import re

from unidecode import unidecode
from webob.exc import strip_tags


def urlify(string):
    """Create a URI-friendly representation of the string
    
    Can be called manually in order to generate an URI-friendly version
    of any string.
    
    """
    s = remove_formatting(string).lower()
    s = replace_whitespace(s, '-')
    return collapse(s, '-')


def remove_formatting(string):
    """Performs multiple text manipulations.
    
    Essentially a shortcut for typing them all. View source below to
    see which methods are run.
    
    """
    s = strip_tags(string)
    s = convert_accented_entities(s)
    s = convert_misc_entities(s)
    s = convert_misc_characters(s)
    return collapse(unidecode(s))


def convert_accented_entities(string):
    """Converts HTML entities into the respective non-accented letters.
    
    Examples:
    
      "&aacute;".convert_accented_entities #: "a"
      "&ccedil;".convert_accented_entities #: "c"
      "&egrave;".convert_accented_entities #: "e"
      "&icirc;".convert_accented_entities #: "i"
      "&oslash;".convert_accented_entities #: "o"
      "&uuml;".convert_accented_entities #: "u"
    
    Note: This does not do any conversion of Unicode/Ascii
    accented-characters. For that functionality please use unidecode.
    
    """
    return re.sub(r'\&([A-Za-z])(grave|acute|circ|tilde|uml|ring|cedil|slash);',
                  r'\1', string)


def convert_misc_entities(string):
    """Converts HTML entities (taken from common Textile formattings) 
    into plain text formats
    
    Note: This isn't an attempt at complete conversion of HTML
    entities, just those most likely to be generated by Textile.
    
    """
    replace_dict = {
        "#822[01]": "\"",
        "#821[67]": "'",
        "#8230": "...",
        "#8211": "-",
        "#8212": "--",
        "#215": "x",
        "gt": ">",
        "lt": "<",
        "(#8482|trade)": "(tm)",
        "(#174|reg)": "(r)",
        "(#169|copy)": "(c)",
        "(#38|amp)": "and",
        "nbsp": " ",
        "(#162|cent)": " cent",
        "(#163|pound)": " pound",
        "(#188|frac14)": "one fourth",
        "(#189|frac12)": "half",
        "(#190|frac34)": "three fourths",
        "(#176|deg)": " degrees"
    }
    for textiled, normal in replace_dict.items():
        string = re.sub(r'\&%s;' % textiled, normal, string)
    return re.sub(r'\&[^;]+;', '', string)


def convert_misc_characters(string):
    """Converts various common plaintext characters to a more
    URI-friendly representation
    
    Examples::
      
        convert_misc_characters("foo & bar") #: "foo and bar"
        convert_misc_characters("Chanel #9") #: "Chanel number nine"
        convert_misc_characters("user@host") #: "user at host"
        convert_misc_characters("google.com") #: "google dot com"
        convert_misc_characters("$10") #: "10 dollars"
        convert_misc_characters("*69") #: "star 69"
        convert_misc_characters("100%") #: "100 percent"
        convert_misc_characters("windows/mac/linux") #: "windows slash mac slash linux"
      
    Note: Because this method will convert any & symbols to the string
    "and", you should run any methods which convert HTML entities 
    (convert_html_entities and convert_misc_entities) before running
    this method.
    
    """
    s = re.sub(r'\.{3,}', " dot dot dot ", string)
    
    # Special rules for money
    money_replace = {
        r'(\s|^)\$(\d+)\.(\d+)(\s|\$)?': r'\2 dollars \3 cents',
        r'(\s|^)£(\d+)\.(\d+)(\s|\$)?': r'\2 pounds \3 pence',
    }
    for repl, subst in money_replace.items():
        s = re.sub(repl, r' %s ' % subst, s)
    
    # Back to normal rules
    repls =  {
        r'\s*&\s*': "and",
        r'\s*#': "number",
        r'\s*@\s*': "at",
        r'(\S|^)\.(\S)': r'\1 dot \2',
        r'(\s|^)\$(\d*)(\s|$)': r'\2 dollars',
        r'(\s|^)£(\d*)(\s|$)': r'\2 pounds',
        r'(\s|^)¥(\d*)(\s|$)': r'\2 yen',
        r'\s*\*\s*': "star",
        r'\s*%\s*': "percent",
        r'\s*(\\|\/)\s*': "slash",
    }
    for repl, subst in repls.items():
        s = re.sub(repl, r' %s ' % subst, s)
    s = re.sub(r"(^|\w)'(\w|$)", r'\1\2', s)
    return re.sub(r"[\.\,\:\;\(\)\[\]\/\?\!\^'\"_]", " ", s)


def replace_whitespace(string, replace=" "):
    """Replace runs of whitespace in string
    
    Defaults to a single space but any replacement string may be
    specified as an argument. Examples::

        replace_whitespace("Foo       bar") # => "Foo bar"
        replace_whitespace("Foo       bar", "-") # => "Foo-bar"
    
    """
    return re.sub(r'\s+', replace, string)
 
def collapse(string, character=" "):
    """Removes specified character from the beginning and/or end of the
    string and then condenses runs of the character within the string.
    
    """
    reg = re.compile('(%s){2,}' % character)
    return re.sub(reg, character, string.strip(character))
