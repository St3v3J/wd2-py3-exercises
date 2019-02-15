import os
import uuid
from smartninja_mongo.connection import MongoClient
from smartninja_mongo.odm import Model

client = MongoClient(os.getenv("MONGODB_URI", "localhost"))  # Find MONGODB_URI env var (Heroku). If not found, use "localhost"
db = client.my_database  # change the database name when you deploy on Heroku
collection = db.users


class User(Model):
    def __init__(self, username, password_hash, **kwargs):
        self.username = username
        self.password_hash = password_hash

        super().__init__(**kwargs)

    def insert(self):
        self.session_token = str(uuid.uuid4())
        user_id = collection.insert_one(self.__dict__).inserted_id
        self._id = user_id  # save id from MongoDB into the User object

        return True

    @classmethod
    def get_by_username(cls, username):
        user_dict = collection.find_one({"username": username})
        user_obj = cls.convert_dict_to_object(data_dict=user_dict)
        return user_obj

    @classmethod
    def get_by_session_token(cls, session_token):
        user_dict = collection.find_one({"session_token": session_token})
        user_obj = cls.convert_dict_to_object(data_dict=user_dict)
        return user_obj

    def set_new_session_token(self):
        self.session_token = str(uuid.uuid4())
        collection.update_one({"_id": self._id}, {"$set": {"session_token": self.session_token}})

        return True
