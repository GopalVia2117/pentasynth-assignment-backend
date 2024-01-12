from flask import Blueprint, jsonify, request
from app.models.file import File
import cloudinary.uploader
from datetime import datetime
from flask_cors import cross_origin


file_bp = Blueprint('file', __name__)

@file_bp.route('/files', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all_files():
    try:
        files = File.get_all()
        return jsonify(files)   
    except:
        return jsonify(message="Internal Server Error"), 500


@file_bp.route('/files', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_file():
    try:
        name = request.form['name']
        size = request.form['size']
        file_type = request.form['type']
        uploadedAt = datetime.now()
        description = request.form["description"]
        media = request.files["file"]
       
        uploaded_media = None
        if(media):
            if file_type.split("/")[0] == "video":
                with media.stream as stream:
                    uploaded_media = cloudinary.uploader.upload_large(stream, resource_type="video")
            else:
                uploaded_media = cloudinary.uploader.upload(media)
            
            if not uploaded_media:
                raise Exception("Upload failed")
            
            print(uploaded_media)
            file_obj = File(name, size, file_type, uploadedAt, description, uploaded_media["secure_url"])
            print(file_obj)
            document = file_obj.save()
            return jsonify(document), 201
        else:
            return jsonify("Media not found"), 400

    except:
        return jsonify("Internal Server Error"), 500



@file_bp.route("/files/<id>", methods=["PUT"])
@cross_origin(supports_credentials=True)
def update_file(id):
    try:
        name = request.form['name']
        description = request.form['description']

        print(name, description)
        updated_document = File.update(id, name, description)
        return jsonify(updated_document), 200

    except:
        return jsonify("Internal Server Error"), 500
    

@file_bp.route("/files/<id>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def delete_file(id):
    try:
        File.delete(id)
        return jsonify("File deleted successfully"), 200
    
    except Exception as e:
        return jsonify("Internal Server Error"), 500


@file_bp.route("/files/search", methods=["GET"])
@cross_origin(supports_credentials=True)
def search_file():
    try:
        term = request.args.get("name")
        documents = File.search(term)
        return jsonify(documents), 200

    except Exception as e:
        return jsonify("Internal Server Error"), 500