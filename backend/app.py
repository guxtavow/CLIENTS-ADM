# ---------------------------------- IMPORTS ----------------------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# ---------------------------------- APP ---------------------------------- 
app = Flask(__name__)
CORS(app)

# ---------------------------------- DATABASE ---------------------------------- 
client = MongoClient("mongodb+srv://dbUser:NePPENpomyF7Kj9F@cluster0.8pzddfi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["user_database"]
collection = db["users"]

# ---------------------------------- ROUTES ---------------------------------- 
@app.route('/users', methods=['GET']) # Get all users
def get_users():
    users = list(collection.find({}, {"_id":0}))
    return jsonify(users)

@app.route('/users/<username>', methods=['GET']) # Get user by username
def get_user(username):
    user = collection.find_one({"username": username}, {"_id":0})
    if user: # Check if user exists
        return jsonify(user)
    else: 
        return jsonify({"message": "User not found"}), 404

@app.route('/new_users', methods=['POST']) # Create new user
def create_user():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "User created successfully"}), 201

@app.route('/update_users/<username>', methods=['PUT']) # Update user
def update_user(username):
    data = request.json
    collection.update_one({"username": username}, {"$set": data})
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/delete_users/<username>', methods=['DELETE']) # Delete user
def delete_user(username):
    collection.delete_one({"username": username})
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    