import requests
import streamlit as st
from typing import List, Dict, Any
import json

# Configuration de l'API
API_BASE_URL = "http://js4g88gcgkkkowks0cg8o40k.147.93.94.113.sslip.io"

def upload_csv_file(file) -> Dict[str, Any]:
    """
    Upload un fichier CSV vers l'API FastAPI
    Le backend utilise l'encodage latin1
    """
    try:
        url = f"{API_BASE_URL}/parquet/upload_file"
        
        # Lire le contenu et le réencoder en latin1 si nécessaire
        file_content = file.getvalue()
        
        # Option 1: Si le fichier est déjà en latin1, on l'envoie tel quel
        # Option 2: Si le fichier est en utf-8, on le convertit
        try:
            # Essayer de décoder en utf-8 puis réencoder en latin1
            decoded = file_content.decode('utf-8')
            encoded_content = decoded.encode('latin1', errors='replace')
            st.info("🔄 Conversion UTF-8 → Latin1 effectuée")
        except UnicodeDecodeError:
            # Si ça échoue, c'est probablement déjà en latin1
            encoded_content = file_content
            st.info("✅ Fichier déjà en Latin1")
        
        # Préparer le fichier pour l'upload
        files = {
            "file": (file.name, encoded_content, "text/csv")
        }
        
        response = requests.post(url, files=files)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'upload: {e}")
        return None

def ask_csv(process_id: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Envoie une question à l'API et récupère la réponse
    messages: [{"role": "human", "content": "question"}]
    """
    try:
        url = f"{API_BASE_URL}/askcsv/double/{process_id}"
        
        payload = {
            "messages": messages
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête: {e}")
        return None

def get_conversation_history(conversation_id: str) -> List[Dict[str, str]]:
    """
    Récupère l'historique des messages depuis Supabase
    """
    from database import get_messages_by_conversation
    return get_messages_by_conversation(conversation_id)