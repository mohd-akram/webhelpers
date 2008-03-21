"""Helper functions ported from Rails"""
from webhelpers.html import literal
from webhelpers.rails.asset_tag import *
from webhelpers.rails.urls import *
from webhelpers.rails.javascript import *
from webhelpers.rails.tags import *
from webhelpers.rails.prototype import *
from webhelpers.rails.scriptaculous import *
from webhelpers.rails.form_tag import *
from webhelpers.rails.secure_form_tag import *
from webhelpers.rails.text import *
from webhelpers.rails.form_options import *
from webhelpers.rails.date import *
from webhelpers.rails.number import *

__pudge_all__ = locals().keys()
__pudge_all__.sort()

from routes import url_for, redirect_to

# Freaky as this may be, it wraps all the HTML tags in literal so they
# continue to work right with systems that recognize literal
def wrap_helpers(localdict):
    def helper_wrapper(func):
        def wrapped_helper(*args, **kw):
            return literal(func(*args, **kw))
        wrapped_helper.__name__ = func.__name__
        return wrapped_helper
    for name, func in localdict.iteritems():
        if not callable(func) or name == 'literal':
            continue
        localdict[name] = helper_wrapper(func)
wrap_helpers(locals())
