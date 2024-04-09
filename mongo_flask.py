from flask import Flask, request, jsonify
from flask_pymongo import PyMongo 
from bson import ObjectId
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://arohan:IccwHydroinformatics12345@nallampatti.f2fnmdo.mongodb.net/CDI?retryWrites=true&w=majority&appName=Nallampatti"

# Configure basic authentication
app.config['BASIC_AUTH_USERNAME'] = 'Kamlesh123'
app.config['BASIC_AUTH_PASSWORD'] = '1234567'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

mongo = PyMongo(app)

# Define the collection name
cdi_collection = mongo.db.cdi


@app.route("/cdi_data", methods=['POST'])
@basic_auth.required
def add_data():
    data = request.json  # Use request.json directly to get JSON data
    cdi_collection.insert_one(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route("/cdi_data", methods=['GET'])
@basic_auth.required
def get_items():
    display_item = []
    for data in cdi_collection.find():
        # Convert ObjectId to string for JSON serialization
        data['_id'] = str(data['_id'])
        display_item.append(data)  
    return jsonify(display_item)

@app.route("/cdi_data/<string:id>", methods=['GET'])  # Changed int to string for ObjectId
@basic_auth.required
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
@basic_auth.required
def update_item(id):
    data = request.json
    result = cdi_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Item updated successfully"})
    else:
        return jsonify({"message": "No item found to update"}), 404

@app.route("/cdi_data/<string:id>", methods=['DELETE'])
@basic_auth.required
def delete_item(id):
    result = cdi_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"message": "No item found to delete"}), 404

if __name__ == '__main__':
    app.run(debug=True)
