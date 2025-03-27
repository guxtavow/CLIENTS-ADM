from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://dbUser:NePPENpomyF7Kj9F@cluster0.8pzddfi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["user_database"]
collection = db["users"]

def clean_timestamp_string(timestamp_str):
    """Remove redundant timezone information from timestamp string"""
    if isinstance(timestamp_str, str):
        # Remove the +00:00 before Z if exists
        return re.sub(r'(\+00:00)(?=Z$)', '', timestamp_str)
    return timestamp_str

def format_timestamp(value):
    """Handle all timestamp formats consistently"""
    if isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value)
        return dt.isoformat() + 'Z'
    
    if isinstance(value, str):
        try:
            # Clean the string first
            clean_str = clean_timestamp_string(value)
            # Parse to datetime object
            dt = datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.isoformat() + 'Z'
        except ValueError:
            try:
                # Try without microseconds
                dt = datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%SZ")
                return dt.isoformat() + 'Z'
            except ValueError:
                pass
    
    # Fallback to current time if parsing fails
    return datetime.now().isoformat() + 'Z'

@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find({}, {"_id": 0}))
    
    for user in users:
        if 'created_ts' in user:
            user['created_ts'] = format_timestamp(user['created_ts'])
        if 'last_updated_at' in user:
            user['last_updated_at'] = format_timestamp(user['last_updated_at'])
    
    return jsonify(users)

#Get specific user
@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = collection.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])
        if "created_at" in user:
            user["created_at"] = user["created_at"].strftime("%d/%m/%Y %H:%M:%S")  
        if "updated_at" in user:
            user["updated_at"] = user["updated_at"].strftime("%d/%m/%Y %H:%M:%S") 
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# CREATE NEW USER
@app.route('/new_users', methods=['POST'])
def create_user():
    data = request.json
    data['created_ts'] = datetime.now().timestamp()
    data['last_updated_at'] = datetime.now().timestamp()
    collection.insert_one(data)
    return jsonify({"message": "User created successfully"}), 201


# UPDATE USER
@app.route('/update_users/<username>', methods=['PUT'])
def update_user(username):
    data = request.json
    
    data.pop('created_ts', None)
    
    # Only update last_updated_at
    data['last_updated_at'] = datetime.now().timestamp()
    
    collection.update_one(
        {"username": username},
        {"$set": data}
    )
    return jsonify({"message": "User updated successfully"}), 200

# DELETE USER
@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    collection.delete_one({"username": username})
    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)