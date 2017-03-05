from pymongo import MongoClient
from bson.objectid import ObjectId


class Note():
    def __init__(
        self, _id=None, user_id=None, date=None, odometr=None, type_to_do=None, info=None,
    ):
        self._id = ObjectId(_id)
        #  тут надо бы как то это обработать
        self.date = date
        # ---
        self.odometr = odometr
        self.type_to_do = type_to_do
        self.info = info
        self.user_id = user_id

    def save(self):
        db = MongoClient().moto

        if self._id:
            db.notes.update_one(
                {'_id': self._id},
                {
                    '$set':
                    {
                        'date': self.date,
                        'odometr': self.odometr,
                        'type_to_do': self.type_to_do,
                        'info': self.info,
                    }
                }
            )

        else:
            db.notes.insert(
                {
                    'date': self.date,
                    'odometr': self.odometr,
                    'type_to_do': self.type_to_do,
                    'info': self.info,
                    'user_id': self.user_id
                }
            )

    def list(self):
        db = MongoClient().moto
        list_of_notes = []
        for note in db.notes.find():
            list_of_notes.append(note)
        return list_of_notes

    def find(self):
        db = MongoClient().moto
        return db.notes.find_one({'_id': self._id})

    def remove(self):
        db = MongoClient().moto
        result = db.notes.delete_one({'_id': self._id})
        return result.deleted_count if result.deleted_count == 1 else None
