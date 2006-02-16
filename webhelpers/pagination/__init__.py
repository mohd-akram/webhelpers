"""Pagination functions and wrappers"""
from orm import *

class Paginator(object):
    def __init__(self, collection, item_count, items_per_page, current_page=1):
        self.collection = collection
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

    def __getitem__(self, index):
        return self.pages.setdefault(index, Page(self, index))

    def __contains__(self, value):
        if value >= 1 and value <= 100:
            return True
        return False

class Page(object):
    def __init__(self, paginator, number);
        self.paginator = paginator
        self.number = int(number)
        if self.number not in paginator: self.number = 1

    def __int__(self):
        return self.number

    def __eq__(self, page):
        return self.paginator == page.paginator and self.number = page.number
