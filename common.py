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


class BaseResource:
    collection_name = None
    model = None

    def __init__(self, db):
        self.db = db
        self.collection = self._get_collection(self.db)

    def save(self, document):
        if document.get('_id'):
            self.collection.update_one(
                {'_id': document.pop('_id')},
                {
                    '$set': document
                }
            )

        else:
            document.pop('_id')
            self.collection.insert(document)

    def list(self):
        list_of_notes = []
        for note in self.collection.find():
            list_of_notes.append(note)
        return list_of_notes

    def find_one(self, document):
        return self.collection.find_one(document['_id'])

    def remove(self, document):
        document = {'_id': document._id}
        result = self.collection.delete_one(document)
        return result.deleted_count if result.deleted_count == 1 else None

    @classmethod
    def _get_collection(cls, db):
        return getattr(db, cls.collection_name)


class MongoPlugin:
    def __init__(self, db, keyword='note_res'):
        self.db = db
        self.keyword = keyword
        self.mongo = None
        self.note_resource = None

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
                self.mongo = getattr(MongoClient(), self.db)
            if not self.note_resource:
                self.note_resource = NoteResource(self.mongo)
            kwargs[self.keyword] = self.note_resource

            result = callback(*args, **kwargs)

            return result

        return wrapper


class NoteResource(BaseResource):
    collection_name = 'notes'
    model = Note


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
