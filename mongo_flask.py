from flask import Flask, request, jsonify
from flask_pymongo import PyMongo 
from bson import ObjectId
import jwt
import datetime
from functools import wraps


app = Flask(__name__)

mongo_uris = {
    'Haridhwar': "mongodb+srv://arohan:IccwHydroinformatics12345@nallampatti.f2fnmdo.mongodb.net/CDI?retryWrites=true&w=majority&appName=Nallampatti",
    'CDI': "mongodb+srv://arohan:IccwHydroinformatics12345@nallampatti.f2fnmdo.mongodb.net/CDI?retryWrites=true&w=majority&appName=Nallampatti",
    'Nallampatti': "mongodb+srv://arohan:IccwHydroinformatics12345@nallampatti.f2fnmdo.mongodb.net/nallampatti?retryWrites=true&w=majority&appName=Nallampatti"
}

SECRET_KEY = 'your_secret_key_here'
app.config['SECRET_KEY'] = SECRET_KEY

# Create separate PyMongo instances for each database
mongo_clients = {db_name: PyMongo(app, uri=mongo_uri) for db_name, mongo_uri in mongo_uris.items()}

# Define collections for each database
cdi_collection = mongo_clients['CDI'].db.cdi
nallampatti_collection = mongo_clients['Nallampatti'].db.livedata
amudala_collection = mongo_clients['CDI'].db.amudala
dadpur_collection = mongo_clients['Haridhwar'].db.dadpur
suman_nagar_collection = mongo_clients['Haridhwar'].db.suman_nagar

@app.route('/')
def home():
    return jsonify({'First_message': 'Hello World'})

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
def add_cdi_data():
    data = request.json  # Use request.json directly to get JSON data
    cdi_collection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route("/cdi_data", methods=['GET'])
@token_required
def get_cdi_items():
    display_item = []
    for data in cdi_collection.find():
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        display_item.append(data)  
    return jsonify(display_item)

@app.route("/cdi_data/<string:id>", methods=['GET'])  # Changed int to string for ObjectId
@token_required
def get_cdi_item(id):
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
def update_cdi_item(id):
    data = request.json
    result = cdi_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "No item found to update"}), 404

@app.route("/cdi_data/<string:id>", methods=['DELETE'])
@token_required
def delete_cdi_item(id):
    result = cdi_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "No item found to delete"}), 404
    

@app.route("/nallampatti_data", methods=['POST'])
@token_required
def add_nallampatti_data():
    data = request.json  # Use request.json directly to get JSON data
    nallampatti_collection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route("/nallampatti_data", methods=['GET'])
@token_required
def get_nallampatti_items():
    display_item = []
    for data in nallampatti_collection.find():
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        display_item.append(data)  
    return jsonify(display_item)

@app.route("/nallampatti_data/<string:id>", methods=['GET'])  # Changed int to string for ObjectId
@token_required
def get_nallampatti_item(id):
    try:
        data = nallampatti_collection.find_one({"_id": ObjectId(id)})  # Convert id to ObjectId
        data['_id'] = str(data['_id'])
        if data:
            return jsonify(data)
        else:
            return jsonify({"message": "Data not found"}), 404
    except:
        return jsonify({"message": "Invalid ID format"}), 400

@app.route("/nallampatti_data/<string:id>", methods=['PUT'])
@token_required
def update_nallampatti_item(id):
    data = request.json
    result = nallampatti_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "No item found to update"}), 404

@app.route("/nallampatti_data/<string:id>", methods=['DELETE'])
@token_required
def delete_nallampatti_item(id):
    result = nallampatti_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "No item found to delete"}), 404  


@app.route("/amudala_data", methods=['POST'])
@token_required
def add_amudala_data():
    data = request.json  # Use request.json directly to get JSON data
    amudala_collection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route("/amudala_data", methods=['GET'])
@token_required
def get_amudala_items():
    display_item = []
    for data in amudala_collection.find():
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        display_item.append(data)  
    return jsonify(display_item)

@app.route("/amudala_data/<string:id>", methods=['GET'])  # Changed int to string for ObjectId
@token_required
def get_amudala_item(id):
    try:
        data = amudala_collection.find_one({"_id": ObjectId(id)})  # Convert id to ObjectId
        data['_id'] = str(data['_id'])
        if data:
            return jsonify(data)
        else:
            return jsonify({"message": "Data not found"}), 404
    except:
        return jsonify({"message": "Invalid ID format"}), 400

@app.route("/amudala_data/<string:id>", methods=['PUT'])
@token_required
def update_amudala_item(id):
    data = request.json
    result = amudala_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "No item found to update"}), 404

@app.route("/amudala_data/<string:id>", methods=['DELETE'])
@token_required
def delete_amudala_item(id):
    result = amudala_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "No item found to delete"}), 404         


@app.route("/dadpur_data", methods=['POST'])
@token_required
def add_dadpur_data():
    data = request.json  # Use request.json directly to get JSON data
    dadpur_collection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route("/dadpur_data", methods=['GET'])
@token_required
def get_dadpur_items():
    display_item = []
    for data in dadpur_collection.find():
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        display_item.append(data)  
    return jsonify(display_item)

@app.route("/dadpur_data/<string:id>", methods=['GET'])  # Changed int to string for ObjectId
@token_required
def get_dadpur_item(id):
    try:
        data = dadpur_collection.find_one({"_id": ObjectId(id)})  # Convert id to ObjectId
        data['_id'] = str(data['_id'])
        if data:
            return jsonify(data)
        else:
            return jsonify({"message": "Data not found"}), 404
    except:
        return jsonify({"message": "Invalid ID format"}), 400

@app.route("/dadpur_data/<string:id>", methods=['PUT'])
@token_required
def update_dadpur_item(id):
    data = request.json
    result = dadpur_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "No item found to update"}), 404

@app.route("/dadpur_data/<string:id>", methods=['DELETE'])
@token_required
def delete_dadpur_item(id):
    result = dadpur_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "No item found to delete"}), 404
    

@app.route("/suman_nagar_data", methods=['POST'])
@token_required
def add_suman_nagar_data():
    data = request.json  # Use request.json directly to get JSON data
    suman_nagar_collection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route("/suman_nagar_data", methods=['GET'])
@token_required
def get_suman_nagar_items():
    display_item = []
    for data in suman_nagar_collection.find():
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        display_item.append(data)  
    return jsonify(display_item)

@app.route("/suman_nagar_data/<string:id>", methods=['GET'])  # Changed int to string for ObjectId
@token_required
def get_suman_nagar_item(id):
    try:
        data = suman_nagar_collection.find_one({"_id": ObjectId(id)})  # Convert id to ObjectId
        data['_id'] = str(data['_id'])
        if data:
            return jsonify(data)
        else:
            return jsonify({"message": "Data not found"}), 404
    except:
        return jsonify({"message": "Invalid ID format"}), 400

@app.route("/suman_nagar_data/<string:id>", methods=['PUT'])
@token_required
def update_suman_nagar_item(id):
    data = request.json
    result = suman_nagar_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "No item found to update"}), 404

@app.route("/suman_nagar_data/<string:id>", methods=['DELETE'])
@token_required
def delete_suman_nagar_item(id):
    result = suman_nagar_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "No item found to delete"}), 404       

if __name__ == '__main__':
    app.run(debug=True)