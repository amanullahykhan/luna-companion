# utils/auth.py
from supabase import create_client, Client
import os

# Load config
from .config import Config

supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)

def login(email: str, password: str):
    """
    Log in user via Supabase Auth (returns user_id or None)
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.user.id
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def signup(email: str, password: str, full_name: str = ""):
    """
    Sign up new user (returns user_id or None)
    """
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name,
                    "preferences": {}
                }
            }
        })
        return response.user.id
    except Exception as e:
        print(f"Signup failed: {e}")
        return None

def get_user_preferences(user_id: str) -> dict:
    """
    Fetch user preferences from Supabase (safe, RLS-protected)
    """
    try:
        res = supabase.table("users").select("*").eq("id", user_id).execute()
        if res.data:
            return res.data[0].get("preferences", {})
    except Exception as e:
        print(f"Get preferences error: {e}")
    return {}

def save_chat(user_id: str, message: str, is_user: bool, metadata: dict = None):
    """
    Save chat to Supabase (RLS ensures user can only write their own data)
    """
    try:
        supabase.table("chats").insert({
            "user_id": user_id,
            "message": message,
            "is_user": is_user,
            "metadata": metadata or {},
        }).execute()
    except Exception as e:
        print(f"Save chat error: {e}")