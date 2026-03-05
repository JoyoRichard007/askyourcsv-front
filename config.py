import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

# Vérification
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ SUPABASE_URL et SUPABASE_KEY doivent être définis")