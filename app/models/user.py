from flask_login import UserMixin
from app import mongo, login_manager
from bson import ObjectId
import bcrypt


class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]
        self.email = user_doc["email"]
        self.role = user_doc.get("role", "viewer")
        self.full_name = user_doc.get("full_name", "")

    @staticmethod
    def find_by_username(username):
        doc = mongo.db.users.find_one({"username": username})
        return User(doc) if doc else None

    @staticmethod
    def find_by_id(user_id):
        doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(doc) if doc else None

    @staticmethod
    def verify_password(username, password):
        doc = mongo.db.users.find_one({"username": username})
        if not doc:
            return None
        if bcrypt.checkpw(password.encode(), doc["password_hash"]):
            return User(doc)
        return None

    @staticmethod
    def create(username, email, password, role="viewer", full_name=""):
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password_hash": pw_hash,
            "role": role,
            "full_name": full_name,
        })


@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)
