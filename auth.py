import bcrypt
import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import logging

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation du client Supabase
@st.cache_resource
def init_supabase():
    """Initialise le client Supabase (mis en cache)"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

def hash_password(password: str) -> str:
    """Hash un mot de passe avec bcrypt"""
    try:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Erreur hash_password: {e}")
        raise

def check_password(password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe correspond au hash"""
    try:
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        logger.error(f"Erreur check_password: {e}")
        return False

def sign_up(email: str, password: str, first_name: str, last_name: str, username: str) -> dict:
    """
    Inscription d'un nouvel utilisateur
    """
    try:
        # Vérifier si l'email existe déjà
        existing = supabase.table("user")\
            .select("id")\
            .eq("email", email)\
            .execute()
        
        if existing.data:
            return {
                "success": False, 
                "error": "Cet email est déjà utilisé. Veuillez vous connecter ou utiliser un autre email."
            }
        
        # Hasher le mot de passe
        hashed = hash_password(password)
        
        # Préparer les données utilisateur
        user_data = {
            "email": email,
            "hashed_password": hashed,
            "first_name": first_name,
            "last_name": last_name,
            "name": username,
            "status": "active",
            "created_at": "now()"
        }
        
        # Insérer dans Supabase
        response = supabase.table("user").insert(user_data).execute()
        
        if response.data:
            user = response.data[0]
            # Ne pas renvoyer le hash
            user.pop("hashed_password", None)
            logger.info(f"Nouvel utilisateur inscrit: {email}")
            return {"success": True, "user": user}
        else:
            return {"success": False, "error": "Erreur lors de l'inscription"}
            
    except Exception as e:
        logger.error(f"Erreur sign_up: {e}")
        return {"success": False, "error": str(e)}

def sign_in(email: str, password: str) -> dict:
    """
    Connexion d'un utilisateur
    """
    try:
        # Chercher l'utilisateur par email
        response = supabase.table("user")\
            .select("*")\
            .eq("email", email)\
            .execute()
        
        if not response.data:
            logger.warning(f"Tentative de connexion avec email inconnu: {email}")
            return {"success": False, "error": "Email ou mot de passe incorrect"}
        
        user = response.data[0]
        
        # Vérifier le mot de passe
        if check_password(password, user["hashed_password"]):
            # Ne pas renvoyer le hash
            user.pop("hashed_password", None)
            logger.info(f"Connexion réussie: {email}")
            return {"success": True, "user": user}
        else:
            logger.warning(f"Mot de passe incorrect pour: {email}")
            return {"success": False, "error": "Email ou mot de passe incorrect"}
            
    except Exception as e:
        logger.error(f"Erreur sign_in: {e}")
        return {"success": False, "error": str(e)}

def sign_out():
    """Déconnexion - vide la session"""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "landing"
    # Optionnel : appeler Supabase auth sign out
    # supabase.auth.sign_out()


def update_user_profile(user_id: str, first_name: str, last_name: str, username: str) -> bool:
    """
    Met à jour le profil utilisateur
    """
    try:
        # Préparer les données à mettre à jour
        update_data = {
            "first_name": first_name,
            "last_name": last_name,
            "name": username,
        }
        
        # Optionnel : Ajouter updated_at si la colonne existe
        # Si vous avez ajouté la colonne, vous pouvez inclure :
        update_data["updated_at"] = "now()"
        
        response = supabase.table("user")\
            .update(update_data)\
            .eq("id", user_id)\
            .execute()
        
        success = bool(response.data)
        if success:
            logger.info(f"Profil mis à jour pour user_id: {user_id}")
        else:
            logger.warning(f"Échec mise à jour profil pour user_id: {user_id}")
            
        return success
        
    except Exception as e:
        logger.error(f"Erreur update_user_profile: {e}")
        return False

def change_password(user_id: str, current_password: str, new_password: str) -> bool:
    """
    Change le mot de passe utilisateur
    """
    try:
        # Récupérer l'utilisateur
        response = supabase.table("user")\
            .select("hashed_password")\
            .eq("id", user_id)\
            .execute()
        
        if not response.data:
            return False
        
        # Vérifier l'ancien mot de passe
        if not check_password(current_password, response.data[0]["hashed_password"]):
            return False
        
        # Hasher le nouveau mot de passe
        new_hashed = hash_password(new_password)
        
        # Mettre à jour
        update = supabase.table("user")\
            .update({"hashed_password": new_hashed})\
            .eq("id", user_id)\
            .execute()
        
        return bool(update.data)
        
    except Exception as e:
        logger.error(f"Erreur change_password: {e}")
        return False

def get_user_profile(user_id: str) -> dict:
    """
    Récupère le profil utilisateur complet
    """
    try:
        response = supabase.table("user")\
            .select("*")\
            .eq("id", user_id)\
            .execute()
        
        if response.data:
            user = response.data[0]
            user.pop("hashed_password", None)  # Ne pas renvoyer le hash
            return user
        return {}
    except Exception as e:
        logger.error(f"Erreur get_user_profile: {e}")
        return {}