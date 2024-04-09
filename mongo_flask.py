from flask import Flask, request, jsonify
from flask_pymongo import PyMongo 
from bson import ObjectId
import jwt
import datetime
from functools import wraps


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://arohan:IccwHydroinformatics12345@nallampatti.f2fnmdo.mongodb.net/CDI?retryWrites=true&w=majority&appName=Nallampatti"

SECRET_KEY = 'your_secret_key_here'

app.config['SECRET_KEY'] = SECRET_KEY


mongo = PyMongo(app)

# Define the collection name
cdi_collection = mongo.db.cdi

# Authentication route to generate JWT token
@app.route('/get_token', methods=['POST'])
def get_token():
    auth_data = request.get_json()  # Assuming JSON data is submitted
    # Check if the username and password are valid
    if auth_data['username'] == 'Kamlesh123' and auth_data['password'] == '1234567':
        # Generate JWT token with username and expiration time
        payload = {
            'username': auth_data["username"],
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=60)
        }

        token = jwt.encode(payload, SECRET_KEY)
        # Return the token as JSON response
        return jsonify({'token': token})
    else:
        # If credentials are invalid, return 401 Unauthorized
        return jsonify({'message': 'Invalid username or password'}), 401
    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401  # Unauthorized
        try:
            # Decode the token without verifying for now to avoid errors if the token is invalid
            data = jwt.decode(token.split(' ')[1], app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401  # Unauthorized
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401  # Unauthorized
        return f(*args, **kwargs)
    return decorated    



@app.route("/cdi_data", methods=['POST'])
@token_required
def add_data():
    data = request.json  # Use request.json directly to get JSON data
    cdi_collection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route("/cdi_data", methods=['GET'])
@token_required
def get_items():
    display_item = []
    for data in cdi_collection.find():
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        display_item.append(data)  
    return jsonify(display_item)

@app.route("/cdi_data/<string:id>", methods=['GET'])  # Changed int to string for ObjectId
@token_required
def get_item(id):
    try:
        data = cdi_collection.find_one({"_id": ObjectId(id)})  # Convert id to ObjectId
        data['_id'] = str(data['_id'])
        if data:
            return jsonify(data)
        else:
            return jsonify({"message": "Data not found"}), 404
    except:
        return jsonify({"message": "Invalid ID format"}), 400

@app.route("/cdi_data/<string:id>", methods=['PUT'])
@token_required
def update_item(id):
    data = request.json
    result = cdi_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "No item found to update"}), 404

@app.route("/cdi_data/<string:id>", methods=['DELETE'])
@token_required
def delete_item(id):
    result = cdi_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "No item found to delete"}), 404

if __name__ == '__main__':
    app.run(debug=True)
