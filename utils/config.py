# utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN", None)  # optional for gated models

    @classmethod
    def validate(cls):
        if not cls.SUPABASE_URL:
            raise ValueError("❌ Missing SUPABASE_URL in environment")
        if not cls.SUPABASE_ANON_KEY:
            raise ValueError("❌ Missing SUPABASE_ANON_KEY in environment")
        if "service_role" in (cls.SUPABASE_ANON_KEY or ""):
            raise ValueError("❌ NEVER use service_role key in frontend!")