def checkbox_group(name, selected_values, options, ncol, 
    direction="horizontal"):
    """Return a group of checkboxes arranged in columns.  See ``group()``.
    """
    return group(name, selected_values, options, ncol, direction, "checkbox")

def radio_group(name, selected_values, options, ncol, 
    direction="horizontal"):
    """Return a group of radio buttons  arranged in columns.  See ``group()``.
    """
    return group(name, selected_values, options, ncol, direction, "radio")


def group(name, selected_values, options, ncol, direction="horizontal",
    input_type="checkbox"):
    """Return a group of checkboxes or radio buttons arranged in columns.

    Arguments:

      ``name`` -- name of the widget group (<input name=>).

      ``selected_values`` -- list or tuple of previously-selected values.
          Pass ``None`` to not select any.

      ``options`` -- a list of ``Option`` objects or ``(value, label)``
          pairs.  See ``select()`` for the range of legal values.

      ``ncol`` -- number of columns.

      ``direction`` -- "horizontal" or "vertical" (or any string starting
          with "h" or "v", case insensitive).  In horizontal groups, the second
          element is to the right of the first.  In vertical groups, the
          second element is below it.

      ``input_type`` -- "checkbox" or "radio".
    """
    if input_type not in ["checkbox", "radio"]:
        raise ValueError("input type must be 'checkbox' or 'radio'")
    if not isinstance(options, Options):
        options = Options(options)
    options_html = [
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
            

