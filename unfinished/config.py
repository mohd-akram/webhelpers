"""Helpers for configuration files."""

### Can be webhelpers.config or webhelpers.configuration module.
def ConfigError(Exception):
    def __init__(self, key, reason, help=None):
        message = "config variable '%s' %s" % (key, message)
        if help:
            message += " (%s)" % help
        Exception.__init__(self, message)


def ConfigLint(object):
    """Check a configuration dict for errors and set default values."""

    def __init__(self, config):
        self.config = config

    def convert_int(self, key):
        """Convert a config variable to integer.  The variable must exist."""
        try:
            self.config[key] = int(self.config[key])
        except ValueError:
            raise ConfigError(key, "must be an integer: %r" % self.config[key])

    def convert_bool(self, key):
        """Convert a config variable to boolean.  The variable must exist."""
        value = self.config[key].strip().lower()
        if value in ["true", "yes", "on", "y", "t", "1"]:
            self.config[key] = True
        elif value in ["false", "no", "off", "n", "f", "0"]:
            self.config[key] = False
        else:
            raise ConfigError(key, "is not true/false: %r" % value)

    def default(self, key, default):
        self.config.setdefault(key, default)

    def default_int(self, key, default):
        if key in self.config:
            self.convert_int(key)
        else:
            self.config[key] = default

    def default_bool(self, key, default):
        if key in self.config:
            self.convert_bool(key)
        else:
            self.config[key] = default

    def require(self, key):
        if key not in self.config:
            raise ConfigError(key, "is required")

    def require_int(self, key):
        self.require(key)
        self.convert_int(key)

    def require_bool(self, key):
        self.require_key(key)
        self.convert_bool(key)

    def require_directory(self, key, create_if_missing=False):
        """Require a directory to exist, optionally creating it if it doesn't.
        """
        self.require(key)
        dir = self.config[key]
        if not os.path.exists(dir) and create_if_missing:
            os.makedirs(dir)
        if not os.path.isdir(dir):
            raise ConfigError(key, "is not a directory")



#### OLDER IMPLEMENTATION ####
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
        

### This is a lower-level alternative to the validation function above, and
### may produce more appropriate error messages.  In Pylons, these functions
### should be called by a fix_config() function called in load_environment()
### in environment.py

class NotGiven(object):
    pass

def require(config, key):
    if key not in config:
        raise KeyError("config variable '%s' is required" % key)

def require_int(config, key, default=NotGiven):
    want_conversion = True
    if key not in config:
        if default is NotGiven:
            raise KeyError("config variable '%s' is required" % key)
        value = default
        want_conversion = False  # Bypass in case default is None.
    if want_conversion:
        try:
            value = int(config[key])
        except ValueError:
            raise ValueError("config variable '%s' must be int" % key)
    config[key] = value
    return value

def require_bool(config, key, default=NotGiven):
    from paste.deploy.converters import asbool
    want_conversion = True
    if key not in config:
        if default is NotGiven:
            raise KeyError("config variable '%s' is required" % key)
        value = default
        want_conversion = False  # Bypass in case default is None.
    if want_conversion:
        try:
            value = asbool(config[key])
        except ValueError:
            tup = key, config[key]
            raise ValueError("config option '%s' is not true/false: %r" % tup)
    config[key] = value
    return value

def require_dir(config, key, create_if_missing=False):
    from unipath import FSPath as Path
    try:
        dir = config[key]
    except KeyError:
        msg = "config option '%s' missing"
        raise KeyError(msg % key)
    dir = Path(config[key])
    if not dir.exists():
        dir.mkdir(parents=True)
    if not dir.isdir():
        msg = ("directory '%s' is missing or not a directory "
               "(from config option '%s')")
        tup = dir, key
        raise OSError(msg % tup)

