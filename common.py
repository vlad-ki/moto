import inspect
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from pandas import to_datetime
from pandas.tslib import NaTType


class DateValueError(ValueError):
    pass


class PluginError(EnvironmentError):
    pass


class Note():
    def __init__(self, _id=None, user_id=None, date=None,
                 odometr=None, type_to_do=None, info=None):
        if date:
            #  check ',' because I think that is a bad in this place in pasdas package
            if ',' in date:
                raise DateValueError
            date = to_datetime(date, errors='coerce')
            if isinstance(date, NaTType):
                raise DateValueError

        self._id = ObjectId(_id) if _id else None
        self.date = datetime(int(date.year), int(date.month), int(date.day)) if date else None
        self.odometr = odometr
        self.type_to_do = type_to_do
        self.info = info
        self.user_id = user_id


class Mongo():
    def __init__(self, db, collection):
        self.db = getattr(MongoClient(), db)
        self.collection = getattr(self.db, collection)

    def save(self, object_):
        kwargs = vars(object_)
        if kwargs.get('_id'):
            self.collection.update_one(
                {'_id': kwargs.pop('_id')},
                {
                    '$set': kwargs
                }
            )

        else:
            kwargs.pop('_id')
            self.collection.insert(kwargs)

    def list(self):
        list_of_notes = []
        for note in self.collection.find():
            list_of_notes.append(note)
        return list_of_notes

    def find_one(self, object_):
        kwargs = vars(object_)['_id']
        return self.collection.find_one(kwargs)

    def remove(self, object_):
        kwargs = {'_id': object_._id}
        result = self.collection.delete_one(kwargs)
        return result.deleted_count if result.deleted_count == 1 else None


class MongoPlugin:
    def __init__(self, db, collection, keyword='mongo'):
        self.db = db
        self.collection = collection
        self.keyword = keyword
        self.mongo = None

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, MongoPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError(
                    "Found another Mongo plugin with "
                    "conflicting settings (non-unique keyword)."
                )

    def apply(self, callback, context):
        args = inspect.getargspec(context.callback)[0]
        if self.keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            if not self.mongo:
                self.mongo = Mongo(self.db, self.collection)
            kwargs[self.keyword] = self.mongo

            result = callback(*args, **kwargs)

            return result

        return wrapper
