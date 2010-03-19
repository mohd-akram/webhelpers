#!/usr/bin/env python
"""Unit tests for unipath.py and unipath_purist.py

Environment variables:
    DUMP : List the contents of test direcories after each test.
    NO_CLEANUP : Don't delete test directories.
(These are not command-line args due to the difficulty of merging my args
with unittest's.)

IMPORTANT: Tests may not assume what the current directory is because the tests
may have been started from anywhere, and some tests chdir to the temprorary
test directory which is then deleted.
"""
import os
import tempfile
import time
import unittest
import sys

from nose.tools import eq_, assert_raises as r

# Package imports
from webhelpers.path import Path

cleanup = not bool(os.environ.get("NO_CLEANUP"))
dump = bool(os.environ.get("DUMP"))

class TestPathConstructor(object):
    def test_args(self):
        eq_(str(Path()), Path.curdir)
        eq_(str(Path("foo/bar.py")), "foo/bar.py")
        eq_(str(Path("foo", "bar.py")), "foo/bar.py")
        eq_(str(Path("foo", "bar", "baz.py")), "foo/bar/baz.py")
        eq_(str(Path("foo", Path("bar", "baz.py"))), "foo/bar/baz.py")
        eq_(str(Path("foo", ["", "bar", "baz.py"])), "foo/bar/baz.py")
        eq_(str(Path("")), "")
        eq_(str(Path()), ".")
        eq_(str(Path("a", 1)), "a/1")

    def test_norm(self):
        eq_(Path("a//b/../c").norm(), "a/c")
        eq_(Path("a/./b").norm(), "a/b")
        eq_(Path("a/./b", norm=True), "a/b")
        eq_(Path("a/./b", norm=False), "a/./b")
        class AutoNormPath(Path):
            auto_norm = True
        eq_(AutoNormPath("a/./b"), "a/b")
        eq_(AutoNormPath("a/./b", norm=True), "a/b")
        eq_(AutoNormPath("a/./b", norm=False), "a/./b")


class TestPath(object):
    def test_repr(self):
        eq_(repr(Path("la_la_la")), "Path('la_la_la')")

    # Not testing expand_user, expand_vars, or expand: too dependent on the
    # OS environment.

    def test_properties(self):
        p = Path("/first/second/third.jpg")
        eq_(p.parent, "/first/second")
        eq_(p.name, "third.jpg")
        eq_(p.ext, ".jpg")
        eq_(p.stem, "third")

    def test_properties2(self):
        p = Path("/usr/lib/python2.5/gopherlib.py")
        eq_(p.parent, Path("/usr/lib/python2.5"))
        eq_(p.name, Path("gopherlib.py"))
        eq_(p.ext, ".py")
        eq_(p.stem, Path("gopherlib"))
        q = Path(p.parent, p.stem + p.ext) 
        eq_(q, p)

    def test_split_root(self):
        eq_(Path("foo/bar.py").split_root(), ("", "foo/bar.py"))
        eq_(Path("/foo/bar.py").split_root(), ("/", "foo/bar.py"))

    def test_split_root_vs_isabsolute(self):
        self.failIf(Path("a/b/c").isabsolute())
        self.failIf(Path("a/b/c").split_root()[0])
        self.assert_(Path("/a/b/c").isabsolute())
        self.assert_(Path("/a/b/c").split_root()[0])
        

    def test_components(self):
        P = Path
        eq_(P("a").components(), [P(""), P("a")])
        eq_(P("a/b/c").components(), [P(""), P("a"), P("b"), P("c")])
        eq_(P("/a/b/c").components(), [P("/"), P("a"), P("b"), P("c")])

    def test_joinpath(self):
        P = Path
        eq_(P("foo/bar", "baz", "fred"), "foo/bar/baz/fred")
        eq_(P("foo/bar", "baz/fred"), "foo/bar/baz/fred")
        eq_(P("foo/bar", "..", "fred"), "foo/bar/../fred")
        eq_(P("foo/bar", ".", "fred"), "foo/bar/./fred")


    def test_child(self):
        Path("foo/bar").child("baz")
        r(UnsafePathError, Path("foo/bar").child, "baz/fred")
        r(UnsafePathError, Path("foo/bar").child, "..", "baz")
        r(UnsafePathError, Path("foo/bar").child, ".", "baz")


class FilesystemTest(object):
    TEST_HIERARCHY = {
        "a_file":  "Nothing important.",
        "animals": {
            "elephant":  "large",
            "gonzo":  "unique",
            "mouse":  "small"},
        "images": {
            "image1.gif": "",
            "image2.jpg": "",
            "image3.png": ""},
        "swedish": {
            "chef": {
                "bork": {
                    "bork": "bork!"}}},
        }

    def setUp(self):
        self.d = d = Path(tempfile.mkdtemp())
        dict2dir(d, self.TEST_HIERARCHY)
        self.a_file = Path(d, "a_file")
        self.animals = Path(d, "animals")
        self.images = Path(d, "images")
        self.chef = Path(d, "swedish", "chef", "bork", "bork")
        if hasattr(self.d, "symlink"):
            self.link_to_chef_file = Path(d, "link_to_chef_file")
            self.link_to_images_dir = Path(d, "link_to_images_dir")
            self.chef.symlink(self.link_to_chef_file)
            self.images.symlink(self.link_to_images_dir)
            self.dead_link = self.d.child("dead_link")
            self.dead_link.write_link("nowhere")
        self.missing = Path(d, "MISSING")
        self.d.chdir()

    def tearDown(self):
        d = self.d
        d.parent.chdir()  # Always need a valid curdir to avoid OSErrors.
        if dump:
            dump_path(d)
        if cleanup:
            d.rmtree()
            if d.exists():
                raise AssertionError("unable to delete temp dir %s" % d)
        else:
            print "Not deleting test directory", d


class TestCalculatingPaths(FilesystemTest):
    def test_inheritance(self):
        assert Path.cwd().name    # Can we access the property?

    def test_cwd(self):
        eq_(str(Path.cwd()), os.getcwd())

    def test_chdir_absolute_relative(self):
        save_dir = Path.cwd()
        self.d.chdir()
        eq_(Path.cwd(), self.d)
        eq_(Path("swedish").absolute(), Path(self.d, "swedish"))
        save_dir.chdir()
        eq_(Path.cwd(), save_dir)

    def test_chef(self):
        p = Path(self.d, "swedish", "chef", "bork", "bork")
        eq_(p.read_file(), "bork!")

    
    def test_absolute(self):
        p1 = Path("images").absolute()
        p2 = self.d.child("images")
        eq_(p1, p2)

    def test_relative(self):
        p = self.d.child("images").relative()
        eq_(p, "images")

    def test_resolve(self):
        p1 = Path(self.link_to_images_dir, "image3.png")
        p2 = p1.resolve()
        eq_(p1.components()[-2:], ["link_to_images_dir", "image3.png"])
        eq_(p2.components()[-2:], ["images", "image3.png"])
        assert p1.exists()
        assert p2.exists()
        assert p1.same_file(p2)
        assert p2.same_file(p1)


def TestRelPathTo(FilesystemTest):
    def test1(self):
        p1 = Path("animals", "elephant")
        p2 = Path("animals", "mouse")
        eq_(p1.rel_path_to(p2), Path("mouse"))
        
    def test2(self):
        p1 = Path("animals", "elephant")
        p2 = Path("images", "image1.gif")
        eq_(p1.rel_path_to(p2), Path(os.path.pardir, "images", "image1.gif"))
        
    def test3(self):
        p1 = Path("animals", "elephant")
        eq_(p1.rel_path_to(self.d), Path(os.path.pardir))
        
    def test3(self):
        p1 = Path("swedish", "chef")
        eq_(p1.rel_path_to(self.d), Path(os.path.pardir, os.path.pardir))
        

class TestHighLevel(FilesystemTest):
    def test_read_file(self):
        eq_(self.chef.read_file(), "bork!")

    # .write_file and .rmtree tested in .setUp.


