"""Helpers for laying out forms (EXPERIMENTAL)

**This module is experimental and subject to change or deletion!**  If you want
to use it in an application, please copy it to the application.

There are various problems with the ``field()`` helper:
- We're not sure if it's correct HTML to put <div> inside a <label> body.
- The title should not be a <label> in the case of radio buttons and
  checkboxes, unless the widget does not have its own label.
- It's not correct for multi-widget fields (e.g., a group of radio buttons
  or checkboxes), because <label>s should not contain multiple input controls
  or other labels.
- Some people prefer the title to the left of the field body, which requires
  either a table or a "style=float:left;width:20em" on the title.
"""

from webhelpers import containers
from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html import tags
from webhelpers.html.tags import NL, BR

__all__ = [
           "field", "form_legend",
           ]

REQUIRED_SYMBOL = HTML.span("*", class_="required-symbol")

def field(title, required, widget, hint=None, error=None, **attrs):
    """A simple non-table formatter for form fields.

    *This helper is still experimental and subject to change. 2008-10-01*

    This helper decorates a form field with its title, required-ness,
    help text, and error message.  It puts the entire field in a 
    *<div class="field">*, which contains the label and an inner
    *<div class="field-body">* containing the error message, input widget,
    and help text.  Visually these are all stacked vertically.    

    If you put multiple widgets in the ``widget`` arg (say a checkbox group
    or radio group), they will all be inside the *<label>*.  This is 
    technically incorrect because a label should contain only one widget.
    If each widget has its own label, there would be a label inside a label.
    We're not sure how to resolve this, so you're on your own for it.

    Arguments:
    ``title`` -- the field title.

    ``required`` -- True if the field must be filled in.  This just affects how
    the field is displayed; you'll have to use Javascript or a server-side
    validator to enforce the constraint.

    ``widget`` -- HTML for the input control. Typically you'd pass the result of
    a form helper or ModelTags helper here.

    ``hint`` -- Extra HTML to display beneath the control.  Typically used for
    help text.  You could also pass invisible Javascript here to make the
    widget more interactive.  Wrap the value in ``literal()`` if it
    contains intentional HTML markup.

    ``error`` -- An error message.  If using FormEncode, leave this at
    the default and instead filter the rendered form through ``htmlfill``.

    ``attrs`` -- Extra HTML attributes for the outermost *<div>*.  By default
    this sets the class to "field".

    
    >>> field("TITLE", True, "WIDGET")
    literal(u'<div class="field">\\n<label><span class="required">TITLE&nbsp;<span class="required-symbol">*</span></span>\\n<div class="field-body">WIDGET</div></label>\\n</div>')
    >>> field("TITLE", False, tags.text("notes"))
    literal(u'<div class="field">\\n<label><span class="not-required">TITLE</span>\\n<div class="field-body"><input name="notes" type="text" /></div></label>\\n</div>')
    >>> field("TITLE", True, tags.text("notes"), "HINT", "ERROR", id="my-id")
    literal(u'<div class="field" id="my-id">\\n<label><span class="required">TITLE&nbsp;<span class="required-symbol">*</span></span>\\n<div class="field-body"><span class="error-message">ERROR</span><br />\\n<input name="notes" type="text" /><br />\\n<div class="hint">HINT</div></div></label>\\n</div>')

    Here's a sample stylesheet to accompany the fields:

    =====

    /* Make sure there's a space above the field. */
    .field {
        margin-top: 1em;
        }

    /* Required symbol (*) is red. */
    .required-symbol {
        color: red;
        font-weight: bold;
        }

    /* Required field labels are bold. */
    .required {
        color: red;
        font-weight: bold;
        }

    /* Non-required fields are normal.  (Set to bold if desired.) */
    .not-required {
        }

    /* The field body is indented under its label. */
    .field-body {
        margin-left: 1em;
        }

    /* Error messages are very obvious: large bold red italic text, with a
     * reddish-pink background and some padding.  */
    .error-message {
        color: #cc0000;
        background-color: #ffeeee;
        font-size: large;
        font-weight: bold;
        font-style: italic;
        padding: 4px;
        }

    /* The hint is green and italic. */
    .hint {
        color: #006400;
        font-style: italic;
        }

    /* Add this class to lay out multiple fields horizontally:
     * field(..., class_="field horizontal")
     * Put the entire row in a <div> to prevent other things from being
     * laid out alongside it. */
    div.horizontal {
        float: left;
        margin-right: 2em;
        }
    =====
    """
    if required:
        title_span = HTML.span(
            title, 
            literal("&nbsp;"),
            REQUIRED_SYMBOL,
            class_="required")
    else:
        title_span = HTML.span(title, class_="not-required")
    body = []
    if error:
        body.append(HTML.span(error, class_="error-message"))
        body.append(BR)
    body.append(widget)
    if hint:
        body.append(BR)
        body.append(HTML.div(hint, class_="hint"))
    attrs.setdefault("class_", "field")
    return HTML.div(
        "\n",
        HTML.label(title_span,
            "\n",
            HTML.div(c=body, class_="field-body"),
            ),
        "\n",
        **attrs)

def form_legend(**attrs):
    """Return a span containing standard form instructions.

    *This helper is experimental and subject to change.  2008-10-01*

    Currently it just explains that "*" means the field is required.

    >>> form_legend()
    literal(u'<span class="required"><span class="required-symbol">*</span> = required</span>')
    >>> form_legend(style="font-size: x-small")
    literal(u'<span class="required" style="font-size: x-small"><span class="required-symbol">*</span> = required</span>')
    """
    attrs.setdefault("class_", "required")
    return HTML.span(
        REQUIRED_SYMBOL,
        " = required",
        **attrs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
