from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from pandas import to_datetime
from pandas.tslib import NaTType


class DateValueError(ValueError):
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
    def __init__(self, db, kollection):
        self.db = getattr(MongoClient(), db)
        self.kollection = getattr(self.db, kollection)

    def save(self, object_):
        kwargs = vars(object_)
        if kwargs.get('_id'):
            self.kollection.update_one(
                {'_id': kwargs.pop('_id')},
                {
                    '$set': kwargs
                }
            )

        else:
            kwargs.pop('_id')
            self.kollection.insert(kwargs)

    def list(self):
        list_of_notes = []
        for note in self.kollection.find():
            list_of_notes.append(note)
        return list_of_notes

    def find_one(self, object_):
        kwargs = vars(object_)['_id']
        return self.kollection.find_one(kwargs)

    def remove(self, object_):
        kwargs = {'_id': object_._id}
        result = self.kollection.delete_one(kwargs)
        return result.deleted_count if result.deleted_count == 1 else None
