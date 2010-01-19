"""Simple object-oriented path manipulations and file read/write.

The ``Path`` object provides properties and methods for accessing path
components and joining paths in an object-oriented manner. It also has a few
filesystem operations for reading and writing a file, and reading symbolic
links.  Path objects are Unicode subclasses, and can be passed to any ``os``
function or third-party library that expects a string filename. (If the
platform can't handle Unicode filenames, Path automatically switches to
``str`` subclasses.)

``webhelpers.path`` is a subset of Mike Orr's ``Unipath`` package, which itself
is based on Jason Orendorff's ``path.py``.  The subset provides the most common
and straightforward path operations for smallish programs that don't want to
depend on a full path library.  It leaves out most filesystem operations such
as listing directories and walking directory trees, and other complex code or
controversial APIs. If you need those, use Python's ``os`` module or install a
complete path library.  (There are several on PyPI -- search for "path" and
"filesystem".)
"""

import os

__all__ = ["Path", "UnsafePathError"]

class UnsafePathError(ValueError):
    pass

# Use unicode strings if possible
_base = os.path.supports_unicode_filenames and unicode or str

class Path(_base):
    """A filesystem path with ``os.path``-like methods."""
    auto_norm = False

    #### Special Python methods.
    def __new__(class_, *args, **kw):
        """Create a path object.

        ``*args`` are one or more string paths, which will be joined using
        ``os.path.join``. An argument can also be a ``Path`` object or a list
        of strings, which will be interpolated and joined.


        Only one keyword argument is allowed, ``norm``.  If ``norm`` is true
        or the class attribute ``.auto_norm`` is true, call ``.norm()`` to
        clean up redundant ".." and ".", double slashes, wrong-direction
        slashes, etc. On case-insensitive filesystems it also converts
        uppercase to lower case. Warning: if the filesystem contains symbolic
        links, normalizing ".." goes to the parent of the symbolic link rather
        than the parent of the linked-to file. Because normalization can 
        sometimes produce a different path than expected, it's disabled by
        default. If you want ``Path`` to always normalize paths, set the 
        ``.auto_norm`` attribute to True at the beginning of your program.
        """

        norm = kw.pop("norm", None)
        if norm is None:
            norm = class_.auto_norm
        if kw:
            kw_str = ", ".join(kw.iterkeys())
            raise TypeError("unrecognized keyword args: %s" % kw_str)
        newpath = class_._new_helper(args)
        if isinstance(newpath, class_):
            return newpath
        if norm:
            newpath = os.path.normpath(newpath)
            # Can't call .norm() because the path isn't instantiated yet.
        return _base.__new__(class_, newpath)

    def __add__(self, more):
        try:
            resultStr = _base.__add__(self, more)
        except TypeError:  #Python bug
            resultStr = NotImplemented
        if resultStr is NotImplemented:
            return resultStr
        return self.__class__(resultStr)
 
    @classmethod
    def _new_helper(class_, args):
        # If no args, return "." or platform equivalent.
        if not args:
            return os.path.curdir
        # Avoid making duplicate instances of the same immutable path
        if len(args) == 1 and isinstance(args[0], class_):
            return args[0]
        legal_arg_types = (class_, basestring, list, int, long)
        args = list(args)
        for i, arg in enumerate(args):
            if not isinstance(arg, legal_arg_types):
                m = "arguments must be str, unicode, list, int, long, or %s"
                raise TypeError(m % class_.__name__)
            if isinstance(arg, (int, long)):
                args[i] = str(arg)
            elif isinstance(arg, class_) and arg.os.path != os.path:
                arg = getattr(arg, components)()   # Now a list.
                if arg[0]:
                    reason = ("must use a relative path when converting "
                              "from '%s' platform to '%s': %s")
                    tup = arg.os.path.__name__, os.path.__name__, arg
                    raise ValueError(reason % tup)
                # Fall through to convert list of components.
            if isinstance(arg, list):
                args[i] = os.path.join(*arg)
        return os.path.join(*args)
        
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, _base(self))

    def norm(self):
        __doc__ = os.path.normpath.__doc__
        return self.__class__(os.path.normpath(self))

    def expand_user(self):
        __doc__ = os.path.expanduser.__doc__
        return self.__class__(os.path.expanduser(self))
    
    def expand_vars(self):
        __doc__ = os.path.expandvars.__doc__
        return self.__class__(os.path.expandvars(self))
    
    def expand(self):
        """Clean up a filename.

        This calls ``.expand_user``, ``.expand_vars``, and ``.norm``
        on the path.  This is commonly everything needed to clean up a filename
        read from a configuration file, for example.
        """
        newpath = os.path.expanduser(self)
        newpath = os.path.expandvars(newpath)
        newpath = os.path.normpath(newpath)
        return self.__class__(newpath)

    #### Properies: parts of the path.

    @property
    def parent(self):
        """The path without the final component; akin to os.path.dirname().
           Example: Path('/usr/lib/libpython.so').parent => Path('/usr/lib')
        """
        return self.__class__(os.path.dirname(self))
    
    @property
    def name(self):
        """The final component of the path.
           Example: path('/usr/lib/libpython.so').name => Path('libpython.so')
        """
        return self.__class__(os.path.basename(self))
    
    @property
    def stem(self):
        """Same as path.name but with one file extension stripped off.
           Example: path('/home/guido/python.tar.gz').stem => Path('python.tar')
        """
        return self.__class__(os.path.splitext(self.name)[0])
    
    @property
    def ext(self):
        """The file extension, for example '.py'."""
        return self.__class__(os.path.splitext(self)[1])

    #### Methods to extract and add parts to the path.

    def ancestor(self, n):
        """Remove ``n`` rightmost components from the path.

        Same as using the ``.parent`` attribute ``n`` times.

        Example:

        >>> p = Path("WebHelpers/html/tags.py")
        >>> p.ancestor(2)
        Path('WebHelpers')
        >>> p.parent.parent
        Path('WebHelpers')
        """
        p = self
        for i in range(n):
            p = os.path.dirname(p)
        return self.__class__(p)

    def joinpath(self, *children):
        """Same as ``os.path.join`` or ``Path(self, \*children)``.

        The children are not checked for special path characters
        ("/", "..", ".").  See ``.child`` for a "safe" version of this 
        method.
        """
        return self.__class__(self, *children)

    def child(self, *children):
        """Join paths in a safe manner.

        >>> Path("/tmp", "foo", "bar.txt")
        Path('/tmp/foo/bar.txt')

        Raise ``UnsafePathError`` if any child contains special path characters
        ("/", "\\", ".", "..").
        """
        for child in children:
            if os.path.sep in child:
                msg = "arg '%s' contains path separator '%s'"
                tup = child, os.path.sep
                raise UnsafePathError(msg % tup)
            if os.path.altsep and os.path.altsep in child:
                msg = "arg '%s' contains alternate path separator '%s'"
                tup = child, os.path.altsep
                raise UnsafePathError(msg % tup)
            if child == os.path.pardir:
                msg = "arg '%s' is parent directory specifier '%s'"
                tup = child, os.path.pardir
                raise UnsafePathError(msg % tup)
            if child == os.path.curdir:    
                msg = "arg '%s' is current directory specifier '%s'"
                tup = child, os.path.curdir
                raise UnsafePathError(msg % tup)
        newpath = os.path.join(self, *children)
        return self.__class__(newpath)

    def norm_case(self):
        __doc__ = os.path.normcase.__doc__
        return self.__class__(os.path.normcase(self))
    
    def isabsolute(self):
        """True if the path is absolute.
           Note that we consider a Windows drive-relative path ("C:foo") 
           absolute even though ntpath.isabs() considers it relative.
        """
        return bool(self.split_root()[0])


    ##### CURRENT DIRECTORY ####
    @classmethod
    def cwd(class_):
        """Return the current working directory as a path object."""
        return class_(os.getcwd())

    #### CALCULATING PATHS ####
    def absolute(self):
        """Return the absolute Path, prefixing the current directory if
           necessary.
        """
        return self.__class__(os.path.abspath(self))

    def relpath(self, start=os.curdir):
        """Make the path relative to ``start`` or the current directory.
        
        Available on Python 2.6 and higher only.
        """
        try:
            p = os.path.relpath(self, start)
        except AttributeError:
            msg = "Path.relpath() is available only on Python 2.6 and higher"
            raise TypeError(msg)
        return self.__class__(p)

    def resolve(self):
        """Return an equivalent Path that does not contain symbolic links."""
        return self.__class__(os.path.realpath(self))

    def strip_parents(self):
        """Remove all directory components from the path in an ultra-safe manner.

        Same as ``p.name``, but also strips Windows-style directory prefixes on
        Unix and vice-versa. Useful for uploaded files, where the remote
        filename shouldn't have a directory prefix but may anyway.
        """
        p = os.path.basename(self)
        # On Unix, strip Windows-style directory prefix manually.
        slash_pos = p.rfind("\\")
        if slash_pos != -1:
            p = p[slash_pos+1:]
        # On Windows, strip Unix-style directory prefix manually.
        slash_pos = p.rfind("/")
        if slash_pos != -1:
            p = p[slash_pos+1:]
        return self.__class__(p)
    
    #### HIGH-LEVEL OPERATIONS ####
    def read_file(self, mode="rU", encoding=None, errors="strict"):
        """Read a file and return the contents.
        
        ``encoding`` and ``errors`` are used to decode the content to Unicode.
        If ``encoding`` is not specified, the bytestring is returned as is.
        """
        f = open(self, mode)
        content = f.read()
        f.close()
        if encoding:
            content = content.encode(encoding, errors)
        return content

    def write_file(self, content, mode="w", encoding=None, errors="strict"):
        """Write a file.
        
        ``encoding`` and ``errors`` are used to encode the content to a 
        bytestring. If ``encoding`` is not specified, the content will be
        written as is, which may raise an exception.
        """
        if encoding:
            content = content.encode(encoding, errors)
        f = open(self, mode)
        f.write(content)
        f.close()

