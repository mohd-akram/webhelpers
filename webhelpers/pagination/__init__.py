"""Pagination functions and wrappers"""
from orm import *

class Paginator(object):
    def __init__(self, item_count, items_per_page=10, current_page=1):
        self.item_count = item_count
        self.items_per_page = items_per_page
        self.pages = {}
        self.current_page = current_page

    def current_page__get(self):
        return self[self.current_page_number]

    def current_page__set(self, page):
        if isinstance(page, Page) and page.paginator != self:
            raise AttributeError("Page/Paginator mismatch")
        page = int(page)
        self.current_page_number = page in self and page or 1
    current_page = property(current_page__get, current_page__set)

    def first_page__get(self):
        return self[1]
    first = first_page = property(first_page__get)
    
    def last_page__get(self):
        return self[self.page_count]
    last = last_page = property(last_page__get)

    def page_count__get(self):
        return (self.item_count == 0) and 1 or (((self.item_count -
            1)//self.items_per_page) + 1)
    __len__ = page_count__get
    page_count = property(page_count__get)

    def __iter__(self):
        for i in range(1, self.page_count + 1):
            yield self[i]

    def __getitem__(self, index):
        return self.pages.setdefault(index, Page(self, index))

    def __contains__(self, value):
        if value >= 1 and value <= self.page_count:
            return True
        return False

class Page(object):
    def __init__(self, paginator, number):
        self.paginator = paginator
        self.number = int(number)
        if self.number not in paginator: self.number = 1

    def __int__(self):
        return self.number

    def __eq__(self, page):
        return self.paginator == page.paginator and self.number == page.number

    def __cmp__(self, page):
        return cmp(self.number, page.number)

    def offset__get(self):
        return self.paginator.items_per_page * (self.number - 1)
    offset = property(offset__get)

    def first_item__get(self):
        return self.offset + 1
    first_item = property(first_item__get)

    def last_item__get(self):
        return min(self.paginator.items_per_page * self.number,
                self.paginator.item_count)
    last_item = property(last_item__get)

    def first__get(self):
        return self == self.paginator.first
    first = property(first__get)

    def last__get(self):
        return self == self.paginator.last
    last = property(last__get)

    def previous__get(self):
        if self.first: return None
        return self.paginator[self.number - 1]
    previous = property(previous__get)

    def next__get(self):
        if self.last: return None
        return self.paginator[self.number + 1]
    next = property(next__get)

    def window(self, padding = 2):
        return Window(self, padding)

class Window(object):
    def __init__(self, page, padding = 2):
        self.paginator = page.paginator
        self.page = page
        self.padding = padding

    def padding__set(self, padding):
        self._padding = padding
        if padding < 0: self._padding = 0
        first_page_in_window = self.page.number - self._padding
        self.first = first_page_in_window in self.paginator and (
        self.paginator[first_page_in_window]) or self.paginator.first
        last_page_in_window = self.page.number + self._padding
        self.last = last_page_in_window in self.paginator and (
        self.paginator[last_page_in_window]) or self.paginator.last

    def padding__get(self):
        return self._padding

    def pages__get(self):
        return [self.paginator[page_number] for page_number in 
            range(self.first.number, self.last.number+1)]
    pages = property(pages__get)
