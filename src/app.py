from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
import cloudinary
import cloudinary.uploader
from datetime import datetime
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
CORS(app, supports_credentials=True)

mongo = PyMongo(app)


cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))



@app.get("/files")
@cross_origin(supports_credentials=True)
def getAllFiles():
    try:
        cursor = mongo.db.file.find().sort([("uploaded_at", -1)])
        documents = []
        for document in cursor:
            document["_id"] = str(document["_id"])
            documents.append(document)
        
        return jsonify(documents)
    except Exception as e:
        return e


@app.post("/files")
@cross_origin(supports_credentials=True)
def createFile():
    try:
        name = request.form['name']
        size = request.form['size']
        file_type = request.form['type']
        uploadedAt = datetime.now()
        description = request.form["description"]
        file = request.files["file"]
        print(file)
        uploaded_file = None
        if(file):
            if file_type.split("/")[0] == "video":
                with file.stream as stream:
                    uploaded_file = cloudinary.uploader.upload_large(stream, resource_type="video")
            else:
                uploaded_file= cloudinary.uploader.upload(file)
            print(uploaded_file)
            document_object = {
                "name": name,
                "size": size,
                "type": file_type,
                "file_url": uploaded_file["secure_url"],
                "description": description,
                "uploaded_at": uploadedAt
            }

            inserted_document = mongo.db.file.insert_one(document_object)
            inserted_id = inserted_document.inserted_id
            document = mongo.db.file.find_one({"_id": inserted_id})
            document["_id"] = str(document["_id"])
            return jsonify(document)
            # return []
        else:
            return jsonify({"error": "File Not Found"})
        
    except Exception as e:
        print(e)
    

@app.route("/files/<id>", methods=["PUT"])
@cross_origin(supports_credentials=True)
def update_file(id):
    try:
        new_name = request.form['name']
        new_description = request.form['description']
        print(new_name, new_description)
        result = mongo.db.file.update_one({"_id": ObjectId(id)}, {"$set": {"name": new_name, "description": new_description}})
        print(result)
        updated_document = mongo.db.file.find_one({"_id": ObjectId(id)})
        updated_document["_id"] = str(updated_document["_id"])
        return jsonify(updated_document)

    
    except:
        return jsonify({"message": "Error updating document"})
        

@app.route("/files/<id>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def delete_file(id):
    try:
        mongo.db.file.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "File deleted successfully"})
    except Exception as e:
        return jsonify({"message": "Error deleting file"})


@app.route("/files/search", methods=["GET"])
@cross_origin(supports_credentials=True)
def search_file():
    try:
        search = request.args.get("name")
        results = mongo.db.file.find({"name": { "$regex" : search}})
        documents = []
        for result in results:
            result["_id"] = str(result["_id"])
            documents.append(result)
        return jsonify(documents)
    except Exception as e:
        return jsonify({"message": "Error deleting file"})
    

@app.get("/test")
@cross_origin(supports_credentials=True)
def test():
    cursor = mongo.db.file.find().sort([("uploaded_at", -1)])
    li = []
    for document in cursor:
        document["_id"] = str(document["_id"])
        li.append(document)

    print(li)
    return jsonify(li)


if __name__ == "__main__":
    app.run(debug=True)