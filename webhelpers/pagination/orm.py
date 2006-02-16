"""ORM Wrappers"""
from webhelpers.util import Partial

orms = {}
try:
    import sqlobject
except:
    pass
else:
    orms['sqlobject'] = True
try:
    import sqlalchemy
except:
    pass
else:
    orms['sqlalchemy'] = True

def get_wrapper(obj, *args, **kw):
    if isinstance(obj, list):
        return obj
    if orms.get('sqlobject'):
        if issubclass(obj, sqlobject.SQLObject):
            return SQLObjectLazy(obj.select, *args, **kw)
    if orms.get('sqlalchemy'):
        return SQLAlchemyLazy(obj.select, *args, **kw)

class SQLObjectLazy(Partial):
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise Exception, "SQLObjectLazy doesn't support getitem without slicing"
        limit = key.stop - key.start + 1
        offset = key.start
        return list(self().limit(limit).offset(offset))
    
    def __len__(self):
        return self().count()

class SQLAlchemyLazy(Partial):
    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise Exception, "SQLAlchemyLazy doesn't support getitem without slicing"
        limit = key.stop - key.start + 1
        offset = key.start
        return self(limit=limit, offset=offset).execute()
    
    def __len__(self):
        pass
