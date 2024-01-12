from flask import Flask, request, jsonify, make_response, session
from datetime import datetime, timedelta
from functools import wraps
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "PsZDQApaeruT0u6bvjWHSA"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=60)
jwt = JWTManager(app)

def token_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return jsonify(message="Token is missing")
        try:
            payload = jwt.decode(token, app.config["secret_key"])
        except:
            return jsonify(message="Invalid token")
    return inner


@app.route("/auth")
@jwt_required()
def auth():
    return jsonify(message="You are in")

@app.route("/login", methods=["POST"])
def login():
    if request.form["username"] and request.form["password"] == "qwertyuiop":
        username = request.form["username"]
        expiration = str(datetime.utcnow() + timedelta(seconds=120))
        
        token = {
            "username": username,
            "expiration": expiration
        }
        try:
            access_token = create_access_token(identity=token)
            return jsonify(access_token=access_token), 200
        
        except Exception as e:
            return jsonify({"error": "Unexpected exception"}), 401





@app.route("/")
def home():
    if not session.get('logged_in'):
        return jsonify(message="Please login first.")
    else:
        return jsonify(message="Logged in currently.")
    

if __name__ == "__main__":
    app.run(debug=True)