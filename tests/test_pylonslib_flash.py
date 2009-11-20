from nose.plugins.skip import SkipTest
from nose.tools import eq_

from webhelpers.pylonslib import Flash, Message

class FakeSession(dict):
    def save(self):
        pass

class TestFlash(object):
    def setUp(self):
        try:
            import pylons
        except ImportError:
            raise SkipTest()
        self._orig_session = pylons.session
        pylons.session = FakeSession()

    def tearDown(self):
        import pylons
        pylons.session = self._orig_session

    def test_flash(self):
        MESSAGE1 = "Record deleted."
        MESSAGE2 = "Hope you didn't need it."
        flash = Flash()
        flash(MESSAGE1)
        flash(MESSAGE2, "warning")
        messages = flash.pop_messages()
        eq_(len(messages), 2)
        eq_(messages[0].message, MESSAGE1)
        eq_(messages[0].category, "notice")
        eq_(messages[1].message, MESSAGE2)
        eq_(messages[1].category, "warning")
        messages = flash.pop_messages()
        eq_(len(messages), 0)

    def test_multiple_flashes(self):
        MESSAGE = "Hello, world!"
        DOOHICKEY_MESSAGE1 = "Added doohickey."
        DOOHICKEY_MESSAGE2 = "Removed doohickey."
        flash = Flash()
        flash2 = Flash("doohickey")
        flash(MESSAGE)
        flash2(DOOHICKEY_MESSAGE1)
        flash2(DOOHICKEY_MESSAGE2)
        messages = flash.pop_messages()
        messages2 = flash2.pop_messages()
        eq_(len(messages), 1)
        eq_(len(messages2), 2)
        eq_(messages[0].message, MESSAGE)
        eq_(messages2[0].message, DOOHICKEY_MESSAGE1)
        messages = flash.pop_messages()
        eq_(len(messages), 0)
        messages2 = flash.pop_messages()
        eq_(len(messages2), 0)
