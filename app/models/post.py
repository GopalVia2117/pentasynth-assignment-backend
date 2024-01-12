from flask_pymongo import pymongo

db = None  # Will be set during initialization

def init_db(app):
    global db
    db = app.mongo.db

class BlogPost:
    @staticmethod
    def create_post(title, content):
        post_data = {"title": title, "content": content}
        db.posts.insert_one(post_data)

    @staticmethod
    def get_all_posts():
        return list(db.posts.find())
