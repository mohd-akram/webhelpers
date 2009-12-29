from nose.tools import eq_

from webhelpers.misc import *

class DummyBase(object):  pass
class Subclass1(DummyBase):  pass
class Subclass2(DummyBase):  pass

def test_subclasses_only():
    subclasses = subclasses_only(DummyBase, globals())
    subclasses.sort()
    control = [Subclass1, Subclass2]
    eq_(subclasses, control)
