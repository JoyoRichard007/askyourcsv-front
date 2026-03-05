# page/csv_list.py
import streamlit as st
from page.sidebar import show_sidebar
from database import get_user_conversations, delete_conversation, get_messages_by_conversation

def show():
    """Page liste des CSV et conversations"""
    
    show_sidebar("csv_list")
    
    st.title("📁 Mes fichiers CSV")
    
    # Récupérer les conversations de l'utilisateur
    user_id = st.session_state.user.get('id')
    conversations = get_user_conversations(user_id)
    
    if not conversations:
        # État vide
        st.info("👋 Vous n'avez pas encore de fichiers CSV")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/4076/4076549.png", width=150)
            st.markdown("### Commencez par importer votre premier fichier CSV")
            if st.button("📤 Importer un CSV", key="empty_import", use_container_width=True):
                st.session_state.page = "import_csv"
                st.rerun()
    
    else:
        # Statistiques RÉELLES
        total_conversations = len(conversations)
        total_messages = sum(len(get_messages_by_conversation(conv['id'])) for conv in conversations)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total fichiers", total_conversations)
        with col2:
            st.metric("Total messages", total_messages)
        with col3:
            last_update = max([conv.get('created_at', '') for conv in conversations]) if conversations else ''
            st.metric("Dernière activité", last_update[:10] if last_update else '-')
        
        st.divider()
        
        # Liste des conversations
        for conv in conversations:
            with st.container():
                cols = st.columns([3, 1, 1, 1, 1])
                
                with cols[0]:
                    st.markdown(f"**{conv.get('name', 'Sans nom')}**")
                    st.caption(f"📄 {conv.get('process_id', '')[:8]}... | 📅 {conv.get('created_at', '')[:10]}")
                
                with cols[1]:
                    # Compter les messages RÉELLEMENT
                    messages = get_messages_by_conversation(conv['id'])
                    msg_count = len(messages)
                    st.metric("Messages", msg_count)
                
                with cols[2]:
                    if st.button("💬 Ouvrir", key=f"open_{conv['id']}", use_container_width=True):
                        st.session_state.current_conversation = conv['id']
                        st.session_state.page = "conversation"
                        st.rerun()
                
                with cols[3]:
                    if st.button("📊 Stats", key=f"stats_{conv['id']}", use_container_width=True):
                        # Afficher des stats sur la conversation
                        with st.expander(f"Statistiques de {conv.get('name')}"):
                            st.write(f"**ID Processus:** {conv.get('process_id')}")
                            st.write(f"**Séparateur:** {conv.get('separator', ';')}")
                            st.write(f"**Créée le:** {conv.get('created_at', '')[:16]}")
                            st.write(f"**Nombre de messages:** {msg_count}")
                
                with cols[4]:
                    if st.button("🗑️", key=f"del_{conv['id']}", help="Supprimer cette conversation"):
                        # ✅ SUPPRESSION EN CASCADE (les messages seront automatiquement supprimés grâce à ON DELETE CASCADE)
                        if delete_conversation(conv['id']):
                            st.success(f"✅ Conversation supprimée avec tous ses messages")
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la suppression")
                
                st.divider()
        
        # Bouton pour importer
        if st.button("📤 Importer un nouveau CSV", key="import_new", use_container_width=True):
            st.session_state.page = "import_csv"
            st.rerun()