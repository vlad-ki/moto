from pymongo import MongoClient
from bson.objectid import ObjectId


class Note():
    def __init__(self, _id=None, user_id=None, date=None,
                 odometr=None, type_to_do=None, info=None):

        self._id = ObjectId(_id) if _id else None
        #  тут надо бы как то это обработать
        self.date = date
        # ---
        self.odometr = odometr
        self.type_to_do = type_to_do
        self.info = info
        self.user_id = user_id


class Mongo():
    def __init__(self, klaster, db):
        self.klaster = getattr(MongoClient(), klaster)
        self.db = getattr(self.klaster, db)

    def save(self, kwargs):
        if kwargs.get('_id'):
            self.db.update_one(
                {'_id': kwargs.pop('_id')},
                {
                    '$set': kwargs
                }
            )

        else:
            kwargs.pop('_id')
            self.db.insert(kwargs)

    def list(self):
        list_of_notes = []
        for note in self.db.find():
            list_of_notes.append(note)
        return list_of_notes

    def find_one(self, kwargs):
        return self.db.find_one(kwargs)

    def remove(self, kwargs):
        result = self.db.delete_one(kwargs)
        return result.deleted_count if result.deleted_count == 1 else None
