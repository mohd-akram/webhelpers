""""Test webhelpers.paginate package."""

from routes import Mapper

from webhelpers.paginate import Page


def test_empty_list():
    """Test whether an empty list is handled correctly."""
    items = []
    page = Page(items, current_page=0)
    assert page.current_page == 0
    assert page.first_item is None
    assert page.last_item is None
    assert page.first_page is None
    assert page.last_page is None
    assert page.previous_page is None
    assert page.next_page is None
    assert page.items_per_page == 20
    assert page.item_count == 0
    assert page.page_count == 0
    assert page.pager() == ''
    assert page.pager(show_if_single_page=True) == ''

def test_one_page():
    """Test that we fit 10 items on a single 10-item page."""
    items = range(10)
    page = Page(items, current_page=0, items_per_page=10)
    assert page.current_page == 1
    assert page.first_item == 0
    assert page.last_item == 9
    assert page.first_page == 1
    assert page.last_page == 1
    assert page.previous_page is None
    assert page.next_page is None
    assert page.items_per_page == 10
    assert page.item_count == 10
    assert page.page_count == 1
    assert page.pager() == ''
    assert page.pager(show_if_single_page=True) == '<span class="pager_curpage">1</span>'

def test_many_pages():
    """Test that 100 items fit on seven 15-item pages."""
    # Create routes mapper so that webhelper can create URLs
    # using webhelpers.url_for()
    mapper = Mapper()
    mapper.connect(':controller')

    items = range(100)
    page = Page(items, current_page=0, items_per_page=15)
    assert page.current_page == 1
    assert page.first_item == 0
    assert page.last_item == 14
    assert page.first_page == 1
    assert page.last_page == 7
    assert page.previous_page is None
    assert page.next_page == 2
    assert page.items_per_page == 15
    assert page.item_count == 100
    assert page.page_count == 7
    assert page.pager() == '<span class="pager_curpage">1</span> <a href="/content?page_nr=2" class="pager_link">2</a> <a href="/content?page_nr=3" class="pager_link">3</a> <span class="pager_dotdot">..</span> <a href="/content?page_nr=7" class="pager_link">7</a>'
    assert page.pager(separator='_') == '<span class="pager_curpage">1</span>_<a href="/content?page_nr=2" class="pager_link">2</a>_<a href="/content?page_nr=3" class="pager_link">3</a>_<span class="pager_dotdot">..</span>_<a href="/content?page_nr=7" class="pager_link">7</a>'
    assert page.pager(link_var='xy') == '<span class="pager_curpage">1</span> <a href="/content?xy=2" class="pager_link">2</a> <a href="/content?xy=3" class="pager_link">3</a> <span class="pager_dotdot">..</span> <a href="/content?xy=7" class="pager_link">7</a>'
    assert page.pager(link_attr={'style':'s1'}, curpage_attr={'style':'s2'}, dotdot_attr={'style':'s3'}) == '<span style="s2">1</span> <a href="/content?page_nr=2" style="s1">2</a> <a href="/content?page_nr=3" style="s1">3</a> <span style="s3">..</span> <a href="/content?page_nr=7" style="s1">7</a>'
    