def checkbox_group(name, selected_values, options, nrows=None):
    """Return a group of checkboxes arranged in columns.  See ``group()``.
    """
    return group(name, selected_values, options, nrows, "checkbox")

def radio_group(name, selected_values, options, nrows):
    """Return a group of radio buttons  arranged in columns.  See ``group()``.
    """
    return group(name, selected_values, options, nrows=None, "radio")


def group(name, selected_values, options, nrows=None, input_type="checkbox"):
    """Return a group of checkboxes or radio buttons arranged in columns.

    The current implementation puts the widgets in an 
    ``<ul class="field-group">``, with a ``<div class="field-group-column">``
    around each column, and a ``<fieldset class="field-group>"`` around the
    whole thing.  You'll have to set an appropriate style for this
    class in order to get the column effect; 
    e.g., "div.field-group-column {float:left, margin-right: 2em}".

    Arguments:

      ``name`` -- name of the widget group (<input name=>).

      ``selected_values`` -- list or tuple of previously-selected values.
          Pass ``None`` to not select any.

      ``options`` -- a list of ``Option`` objects or ``(value, label)``
          pairs.  See ``select()`` for the range of legal values.

      ``nrows`` -- number of rows (i.e., max number of widgets per column).

      ``input_type`` -- "checkbox" or "radio".
    """
    if input_type not in ["checkbox", "radio"]:
        raise ValueError("input type must be 'checkbox' or 'radio'")
    if not isinstance(options, Options):
        options = Options(options)
    html_options = [
        HTML.label(
            HTML.input(type=input_type, name=name, value=x.value),
            x.label)
        for x in options]
    # Distribute the elements horizontally or vertically into a 2D list
    # in row-major order.
    array = containers.distribute(options_html, ncol, direction)
    # Turn the list sideways to make it column-major.
    columns = containers.transpose(array)
    # Format each column into a <div>.
    for i, col in enumerate(columns):
        col = BR.join(columns[i])
        columns[i] = HTML.div(c=col, style="float:left; margin-right: 2em")
    return HTML.div(NL, NL.join(columns), NL)
            

