# data_utils.py - Shared data functions
from data_utils import load_users, load_feedback
import json

def load_users():
    try:
        with open("users_db.json", "r") as f:
            return json.load(f)
    except:
        return {}

def load_feedback():
    try:
        with open("feedback.json", "r") as f:
            return json.load(f)
    except:
        return []
