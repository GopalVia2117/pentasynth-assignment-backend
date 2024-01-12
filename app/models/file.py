from app import db
from bson.objectid import ObjectId

class File:
    name = None
    size = None
    file_type = None
    uploaded_at = None
    description = None
    file_url = None

    def __init__(self, name, size, file_type, uploaded_at, description, url):
        self.name = name
        self.size = size
        self.file_type = file_type
        self.uploaded_at = uploaded_at
        self.description = description
        self.file_url = url


    def save(self):
        print("saving.....")
        try:
            document_object = {
            "name": self.name,
            "size": self.size,
            "type": self.file_type,
            "uploaded_at": self.uploaded_at,
            "description": self.description,
            "file_url": self.file_url
            }

            print(document_object)

            inserted_document = db.file.insert_one(document_object)
            print(inserted_document)
            inserted_id = inserted_document.inserted_id
            document = db.file.find_one({"_id": inserted_id})
            document["_id"] = str(document["_id"])
            
            return document
        
        except:
            raise Exception("Could not save")
        

    @staticmethod
    def get_all():
        try:
            cursor = db.file.find({})
            documents = []
            for document in cursor:
                document["_id"] = str(document["_id"])
                documents.append(document)  
            return documents
        
        except:
            raise Exception("Internal server error")
    
    @staticmethod
    def update(id, name, description):
        try:
            result = db.file.update_one({"_id": ObjectId(id)}, {"$set": {"name": name, "description": description}})
            print(result)
            updated_document = db.file.find_one({"_id": ObjectId(id)})
            updated_document["_id"] = str(updated_document["_id"])
            return updated_document
        
        except:
            raise Exception("Internal server error")

    @staticmethod
    def delete(id):
        try:
            db.file.delete_one({"_id": ObjectId(id)})
            return
        except:
            raise Exception("Internal server error")

    @staticmethod
    def search(term):
        try:
            results = db.file.find({"name": { "$regex" : term}})
            documents = []
            for result in results:
                result["_id"] = str(result["_id"])
                documents.append(result)
            return documents
        except:
            raise Exception("Internal server error")