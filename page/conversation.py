# page/conversation.py
import streamlit as st
from page.sidebar import show_sidebar
from api import ask_csv
from database import get_messages_by_conversation, add_message, get_user_conversations
from datetime import datetime

def show():
    """Page de conversation avec l'IA"""
    
    show_sidebar("conversation")
    
    # Vérifier si une conversation est sélectionnée
    if "current_conversation" not in st.session_state:
        st.session_state.current_conversation = None
    
    # Si pas de conversation sélectionnée, afficher la liste
    if not st.session_state.current_conversation:
        show_conversations_list()
        return
    
    # Afficher la conversation
    show_conversation(st.session_state.current_conversation)

def show_conversations_list():
    """Affiche la liste des conversations"""
    
    st.title("💬 Mes conversations")
    
    # Récupérer les conversations
    conversations = get_user_conversations(st.session_state.user.get('id'))
    
    if not conversations:
        st.info("👋 Vous n'avez pas encore de conversations")
        if st.button("📤 Importer un CSV pour commencer", use_container_width=True):
            st.session_state.page = "import_csv"
            st.rerun()
        return
    
    # Statistiques
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total conversations", len(conversations))
    with col2:
        if st.button("➕ Nouvelle conversation", use_container_width=True):
            st.session_state.page = "import_csv"
            st.rerun()
    
    st.divider()
    
    # Liste des conversations
    for conv in conversations:
        with st.container():
            cols = st.columns([4, 1, 1])
            
            with cols[0]:
                st.markdown(f"**{conv.get('name', 'Sans nom')}**")
                st.caption(f"📁 {conv.get('process_id', '')[:8]}... | 📅 {conv.get('created_at', '')[:10]}")
            
            with cols[1]:
                # Récupérer le nombre de messages
                messages = get_messages_by_conversation(conv['id'])
                st.metric("Messages", len(messages) // 2 if messages else 0)
            
            with cols[2]:
                if st.button("Ouvrir", key=f"open_conv_{conv['id']}", use_container_width=True):
                    st.session_state.current_conversation = conv['id']
                    st.rerun()
            
            st.divider()

def show_conversation(conversation_id):
    """Affiche une conversation spécifique"""
    
    # En-tête avec bouton retour
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Retour", key="back_to_list"):
            st.session_state.current_conversation = None
            st.rerun()
    with col2:
        # Récupérer les infos de la conversation
        conversations = get_user_conversations(st.session_state.user.get('id'))
        current_conv = next((c for c in conversations if c['id'] == conversation_id), {})
        st.title(f"💬 {current_conv.get('name', 'Conversation')}")
    
    # Récupérer l'historique
    messages = get_messages_by_conversation(conversation_id)
    
    # Afficher les messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("created_at"):
                st.caption(msg["created_at"][:16])
    
    # Zone de saisie
    if prompt := st.chat_input("Posez votre question sur les données..."):
        # Afficher le message utilisateur
        with st.chat_message("user"):
            st.write(prompt)
        
        # Sauvegarder dans la base
        next_index = len(messages)
        add_message(conversation_id, "human", prompt, next_index)
        
        # Mettre à jour la liste des messages pour la suite
        messages.append({"role": "human", "content": prompt})
        
        # Préparer l'historique pour l'API
        api_messages = []
        for msg in messages:
            role = "human" if msg["role"] == "human" else "assistant"
            api_messages.append({"role": role, "content": msg["content"]})
        
        # Récupérer le process_id
        process_id = current_conv.get('process_id')
        
        if not process_id:
            st.error("Erreur: ID de processus non trouvé")
            return
        
        # Appeler l'API
        with st.spinner("Analyse en cours..."):
            result = ask_csv(process_id, api_messages)
            
            if result and "messages" in result:
                # Récupérer la réponse
                assistant_msg = result["messages"][-1]
                response = assistant_msg.get("content", "Désolé, je n'ai pas pu analyser votre question.")
                
                # Afficher la réponse
                with st.chat_message("assistant"):
                    st.write(response)
                
                # Sauvegarder dans la base
                add_message(conversation_id, "assistant", response, next_index + 1)
                
                # ✅ PLUS DE st.rerun() ici - on laisse l'affichage se faire naturellement
            else:
                st.error("❌ Erreur lors de l'analyse")