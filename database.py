# database.py
import logging
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import streamlit as st

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation du client Supabase
@st.cache_resource
def init_supabase():
    """Initialise le client Supabase (mis en cache)"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# ============================================
# FONCTIONS POUR LES CONVERSATIONS
# ============================================

def create_conversation(user_id: str, file_id: str, file_name: str, separator: str, name: str = None) -> dict:
    """
    Crée une nouvelle conversation après upload de fichier
    """
    try:
        conversation_data = {
            "user_id": user_id,
            "process_id": file_id,  # Le file_id de l'API devient process_id
            "name": name or file_name,
            "separator": separator,
            "created_at": "now()"
        }
        
        response = supabase.table("conversation").insert(conversation_data).execute()
        
        if response.data:
            logger.info(f"Conversation créée pour user_id: {user_id}")
            return {"success": True, "conversation": response.data[0]}
        return {"success": False, "error": "Erreur création conversation"}
        
    except Exception as e:
        logger.error(f"Erreur create_conversation: {e}")
        return {"success": False, "error": str(e)}

def get_user_conversations(user_id: str) -> list:
    """
    Récupère toutes les conversations d'un utilisateur
    """
    try:
        response = supabase.table("conversation")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()
        
        conversations = response.data if response.data else []
        logger.info(f"Récupéré {len(conversations)} conversations pour user_id: {user_id}")
        return conversations
        
    except Exception as e:
        logger.error(f"Erreur get_user_conversations: {e}")
        return []

def get_conversation(conversation_id: str) -> dict:
    """
    Récupère une conversation par son ID
    """
    try:
        response = supabase.table("conversation")\
            .select("*")\
            .eq("id", conversation_id)\
            .execute()
        
        return response.data[0] if response.data else None
        
    except Exception as e:
        logger.error(f"Erreur get_conversation: {e}")
        return None

def delete_conversation(conversation_id: str) -> bool:
    """
    Supprime une conversation et ses messages (CASCADE)
    """
    try:
        response = supabase.table("conversation")\
            .delete()\
            .eq("id", conversation_id)\
            .execute()
        
        success = bool(response.data)
        if success:
            logger.info(f"Conversation {conversation_id} supprimée")
        return success
        
    except Exception as e:
        logger.error(f"Erreur delete_conversation: {e}")
        return False

# ============================================
# FONCTIONS POUR LES MESSAGES
# ============================================

def add_message(conversation_id: str, role: str, content: str, index: int) -> dict:
    """
    Ajoute un message à une conversation
    """
    try:
        message_data = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "index": index,
            "created_at": "now()"
        }
        
        response = supabase.table("message").insert(message_data).execute()
        
        if response.data:
            logger.info(f"Message ajouté à conversation {conversation_id}")
            return {"success": True, "message": response.data[0]}
        return {"success": False, "error": "Erreur ajout message"}
        
    except Exception as e:
        logger.error(f"Erreur add_message: {e}")
        return {"success": False, "error": str(e)}

def get_messages_by_conversation(conversation_id: str) -> list:
    """
    Récupère tous les messages d'une conversation
    """
    try:
        response = supabase.table("message")\
            .select("*")\
            .eq("conversation_id", conversation_id)\
            .order("index")\
            .execute()
        
        messages = response.data if response.data else []
        logger.info(f"Récupéré {len(messages)} messages pour conversation {conversation_id}")
        return messages
        
    except Exception as e:
        logger.error(f"Erreur get_messages_by_conversation: {e}")
        return []

def delete_messages_by_conversation(conversation_id: str) -> bool:
    """
    Supprime tous les messages d'une conversation
    """
    try:
        response = supabase.table("message")\
            .delete()\
            .eq("conversation_id", conversation_id)\
            .execute()
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur delete_messages_by_conversation: {e}")
        return False
def get_messages_by_conversation(conversation_id: str) -> list:
    """
    Récupère tous les messages d'une conversation
    """
    try:
        response = supabase.table("message")\
            .select("*")\
            .eq("conversation_id", conversation_id)\
            .order("index")\
            .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        logger.error(f"Erreur get_messages_by_conversation: {e}")
        return []