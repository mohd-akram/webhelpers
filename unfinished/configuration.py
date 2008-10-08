"""Helpers for configuring an application."""

import os

class ConfigError(Exception):
    def __init__(self, key, reason, help=None):
        message = "config variable '%s' %s" % (key, reason)
        if help:
            message += " (%s)" % help
        Exception.__init__(self, message)


class ConfigLint(object):
    """Check a configuration dict for errors and set default values."""

    def __init__(self, config, filename=None, section=None):
        self.config = config
        self.filename = os.path.abspath(filename)
        self.section = section

    def convert_int(self, key):
        """Convert a config variable to integer.  The variable must exist."""
        try:
            self.config[key] = int(self.config[key])
        except ValueError:
            self._error(key, "must be an integer: %r" % self.config[key])

    def convert_bool(self, key):
        """Convert a config variable to boolean.  The variable must exist."""
        value = self.config[key].strip().lower()
        if value in ["true", "yes", "on", "y", "t", "1"]:
            self.config[key] = True
        elif value in ["false", "no", "off", "n", "f", "0"]:
            self.config[key] = False
        else:
            self._error(key, "is not true/false: %r" % value)

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
            self._error(key, "is required")

    def require_int(self, key):
        self.require(key)
        self.convert_int(key)

    def require_bool(self, key):
        self.require(key)
        self.convert_bool(key)

    def require_directory(self, key, create_if_missing=False):
        """Require a directory to exist, optionally creating it if it doesn't.
        """
        self.require(key)
        dir = self.config[key]
        if not os.path.exists(dir) and create_if_missing:
            os.makedirs(dir)
        if not os.path.isdir(dir):
            self._error(key, "is not a directory")

    # Private methods
    def _error(self, key, reason):
        if self.filename:
            reason += " in file '%s'" % self.filename
            if self.section:
                reason += " section '%s'" % self.section
        raise ConfigError(key, reason)
