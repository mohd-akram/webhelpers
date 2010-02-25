import os

class OverwriteError(EnvironmentError):
    """Refusing to overwrite an existing file or directory.
    
    Usage:
    >> raise OverwriteError("OUTPUT")
    OverwriteError: not overwriting file '/home/me/OUTPUT'
    >> raise OverwriteError("/tmp", "output")
    OverwriteError: not overwriting output directory '/tmp'

    It will use the ``os`` module to get the full path and determine
    whether the existing file is a directory.
    """

    def __init__(self, filename, what=""):
        self.filename = filename
        self.what = what
        filetype = "file"
        try:
            if os.path.isdir(filename):
                filetype = "directory"
        except IOError:
            pass
        words = []
        words.append("not overwriting")
        if what:
            words.append(what)
        if filetype:
            words.append(filetype)
        words.append("'%s'" % os.path.abspath(filename))
        msg = " ".join(words)
        EnvironmentError.__init__(self, msg)

