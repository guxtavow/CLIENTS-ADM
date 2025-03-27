# Importing libraries
import json
from dataclasses import dataclass
from datetime import datetime
from pymongo import MongoClient

# Configs of the database
client = MongoClient("mongodb+srv://dbUser:NePPENpomyF7Kj9F@cluster0.8pzddfi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["user_database"]
collection = db["users"]

# Def funcions
def timestamp_convert(date_str):
    try: # Try to convert the date string to a timestamp
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.timestamp()
    except: # If the conversion fails, return None
        return None
    
def roles_convert(info): # Convert the roles to a list
    roles = [] # Create an empty list
    # Add the roles to the list according to the boolean values
    if info["is_user_admin"]:
        roles.append("admin")
    if info["is_user_manager"]:
        roles.append("manager")
    if info["is_user_tester"]:
        roles.append("tester")
    return roles


# DataClass Definitions
@dataclass
class UserPreferences:
    timezone: str
    
    def to_dict(self): # Convert the dataclass to a dictionary
        return {
            "timezone": self.timezone
        }
@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_ts: float
    active: bool = True


def parse_user_data(json_file): # creating function for parsing
    # Process the JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    users = []  # creating a list of users that will receive the formatted data

    # Iterate over the JSON data
    for info in data["users"]:
        #variables 
        created_ts = timestamp_convert(info["created_at"])    
        roles = roles_convert(info)
        
        # Check if the user already exists based on username
        existing_user = collection.find_one({"username": info["user"]})
        if existing_user:
            print(f"User {info['user']} already exists. Skipping insertion.")
            continue
        
        # Create the User object
        user = User(
            username=info["user"],
            password=info["password"],
            roles=roles,
            preferences=UserPreferences(timezone=info["user_timezone"]).to_dict(),
            active=info["is_user_active"],
            created_ts= created_ts
        )
        
        # Add the User object to the list
        users.append(user)

    # Insert users into the database
    if users:
        try:
            collection.insert_many([user.__dict__ for user in users])
            print("Users inserted into the database!")
        except Exception as e:
            print(f"Error inserting into MongoDB: {e}")
    else:
        print("No valid users to insert.")
        
    return users

parse_user_data("udata.json") # calling function