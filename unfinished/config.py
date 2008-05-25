"""Helpers for configuration files."""

class ConfigurationError(Exception):
    pass

def validate_config(config, validator, filename=None):
    """Validate an application's configuration.

    ``config`` 
        A dict-like object containing configuration values.

    ``validator``
        A FormEncode `Schema``.  A ``FancyValidator`` is also acceptable if it
        operates on a dict of values (not on a single value) and raises
        ``Invalid`` with a dict of error messages (not a single error message).

    ``filename``
        The configuration file's path if known.  Paste users should pass
        ``config.__file__`` here.

    This helper depends on Ian Bicking's FormEncode package.
    """
    from formencode import Invalid
    try:
        return validator.to_python(config)
    except Invalid, e:
        if filename:
            message = "configuration file '%s'" % filename
        else:
            message = "the application configuration"
        message += " has the following errors: "
        lines = [message]
        for key, error in sorted(e.error_dict.iteritems()):
            message = "    %s: %s" % (key, error)
            lines.append(message)
        message = "\n".join(lines)
        raise ConfigurationError(message)
        
