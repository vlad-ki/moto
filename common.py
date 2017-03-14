import inspect
from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil.parser import parse


class DateValueError(ValueError):
    pass


class PluginError(EnvironmentError):
    pass


class Note():
    def __init__(self, _id=None, user_id=None, date=None,
                 odometr=None, type_to_do=None, info=None):

        self._id = ObjectId(_id) if _id else None
        self.date = date
        self.odometr = odometr
        self.type_to_do = type_to_do
        self.info = info
        self.user_id = user_id


class Mongo():
    def __init__(self, db, collection):
        self.db = getattr(MongoClient(), db)
        self.collection = getattr(self.db, collection)

    def save(self, object_):
        if object_.get('_id'):
            self.collection.update_one(
                {'_id': object_.pop('_id')},
                {
                    '$set': object_
                }
            )

        else:
            object_.pop('_id')
            self.collection.insert(object_)

    def list(self):
        list_of_notes = []
        for note in self.collection.find():
            list_of_notes.append(note)
        return list_of_notes

    def find_one(self, object_):
        return self.collection.find_one(object_['_id'])

    def remove(self, object_):
        object_ = {'_id': object_._id}
        result = self.collection.delete_one(object_)
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


def date_parse(date):
    try:
        return parse(date)
    except ValueError:
        raise DateValueError


def note_object_to_dict(note):
    if isinstance(note, Note):
        return {
            '_id': note._id,
            'user_id': note.user_id,
            'date': note.date,
            'odometr': note.odometr,
            'type_to_do': note.type_to_do,
            'info': note.info
        }
    else:
        raise TypeError(
            'argument of "note_object_to_dict" function must be object of "Note" class')
