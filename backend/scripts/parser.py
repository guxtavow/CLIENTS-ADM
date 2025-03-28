# Importing libraries
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pymongo import MongoClient, UpdateOne
from typing import Optional


# Configs of the database
client = MongoClient("mongodb+srv://dbUser:NePPENpomyF7Kj9F@cluster0.8pzddfi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["user_database"]
collection = db["users"]

# Helper functions
def timestamp_convert(date_str: str) -> Optional[float]:
    """Convert ISO format string to timestamp"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.replace(tzinfo=timezone.utc).timestamp()
    except (ValueError, TypeError):
        return None
    
def roles_convert(info: dict) -> list:
    """Convert role booleans to role list"""
    roles = []
    if info.get("is_user_admin"):
        roles.append("admin")
    if info.get("is_user_manager"):
        roles.append("manager")
    if info.get("is_user_tester"):
        roles.append("tester")
    return roles

def format_timestamp(ts: float) -> str:
    """Convert timestamp to ISO format string"""
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# DataClass Definitions
@dataclass
class UserPreferences:
    timezone: str
    
    def to_dict(self):
        return asdict(self)

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    created_ts: float
    last_updated_at: Optional[float] = None
    active: bool = True

    def to_dict(self):
        data = asdict(self)
        data['preferences'] = self.preferences.to_dict()
        return data

def parse_user_data(json_file: str, update_existing: bool = False):
    """Process JSON file and insert/update users in database"""
    with open(json_file, "r") as f:
        data = json.load(f)

    operations = []

    for info in data["users"]:
        created_ts = timestamp_convert(info["created_at"]) or datetime.now(timezone.utc).timestamp()
        roles = roles_convert(info)
        
        # Create update operation
        operation = {
            'filter': {'username': info["user"]},
            'update': {
                '$set': {
                    'roles': roles,
                    'preferences': {'timezone': info["user_timezone"]},
                    'active': info["is_user_active"],
                    'last_updated_at': datetime.now(timezone.utc).timestamp()
                },
                '$setOnInsert': {
                    'created_ts': created_ts,
                    'password': info["password"]
                }
            },
            'upsert': True
        }
        operations.append(UpdateOne(**operation))

    if operations:
        try:
            result = collection.bulk_write(operations)
            print(f"Successfully updated {result.modified_count} users")
            print(f"Inserted {result.upserted_count} new users")
        except Exception as e:
            print(f"Database operation failed: {str(e)}")
            

parse_user_data("../udata.json", update_existing=True)
