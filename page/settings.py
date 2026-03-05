# page/settings.py
import streamlit as st
from datetime import datetime
from auth import update_user_profile, change_password, get_user_profile
from database import get_user_conversations, delete_conversation, get_messages_by_conversation  
from page.sidebar import show_sidebar

def show():
    """Page des paramètres utilisateur"""
    
    show_sidebar("settings")
    
    st.title("⚙️ Paramètres")
    
    # Récupérer les données réelles
    user_id = st.session_state.user.get('id')
    conversations = get_user_conversations(user_id)
    
    # Calculer les statistiques réelles
    total_conversations = len(conversations)
    total_messages = 0
    for conv in conversations:
        total_messages += len(get_messages_by_conversation(conv['id']))
    
    # Estimer l'espace utilisé (simulé - à adapter selon vos besoins)
    estimated_size = total_messages * 0.5  # 0.5 KB par message en moyenne
    
    # Créer des onglets (Notifications supprimé)
    tab1, tab2, tab3 = st.tabs(["👤 Profil", "🔐 Sécurité", "🗑️ Données"])
    
    # ============================================
    # ONGLET 1 : PROFIL (inchangé)
    # ============================================
    with tab1:
        st.subheader("Informations personnelles")
        
        if st.session_state.user:
            user = st.session_state.user
            
            with st.form("profile_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_first_name = st.text_input(
                        "Prénom", 
                        value=user.get('first_name', ''),
                        key="settings_firstname"
                    )
                
                with col2:
                    new_last_name = st.text_input(
                        "Nom", 
                        value=user.get('last_name', ''),
                        key="settings_lastname"
                    )
                
                new_username = st.text_input(
                    "Nom d'utilisateur", 
                    value=user.get('name', ''),
                    key="settings_username"
                )
                
                st.text_input(
                    "Email", 
                    value=user.get('email', ''),
                    disabled=True,
                    key="settings_email"
                )
                
                st.markdown("---")
                
                submitted = st.form_submit_button("💾 Mettre à jour le profil", use_container_width=True)
                
                if submitted:
                    success = update_user_profile(
                        user_id=user.get('id'),
                        first_name=new_first_name,
                        last_name=new_last_name,
                        username=new_username
                    )
                    
                    if success:
                        st.success("✅ Profil mis à jour avec succès !")
                        st.session_state.user['first_name'] = new_first_name
                        st.session_state.user['last_name'] = new_last_name
                        st.session_state.user['name'] = new_username
                    else:
                        st.error("❌ Erreur lors de la mise à jour")
    
    # ============================================
    # ONGLET 2 : SÉCURITÉ (inchangé)
    # ============================================
    with tab2:
        st.subheader("Changer le mot de passe")
        
        with st.form("password_form"):
            current_password = st.text_input(
                "Mot de passe actuel", 
                type="password",
                key="settings_current_password"
            )
            
            new_password = st.text_input(
                "Nouveau mot de passe", 
                type="password",
                key="settings_new_password"
            )
            
            confirm_password = st.text_input(
                "Confirmer le nouveau mot de passe", 
                type="password",
                key="settings_confirm_password"
            )
            
            st.markdown("---")
            
            password_submitted = st.form_submit_button("🔑 Changer le mot de passe", use_container_width=True)
            
            if password_submitted:
                if not current_password or not new_password or not confirm_password:
                    st.error("Veuillez remplir tous les champs")
                elif new_password != confirm_password:
                    st.error("Les nouveaux mots de passe ne correspondent pas")
                elif len(new_password) < 6:
                    st.error("Le mot de passe doit contenir au moins 6 caractères")
                else:
                    success = change_password(
                        user_id=st.session_state.user.get('id'),
                        current_password=current_password,
                        new_password=new_password
                    )
                    
                    if success:
                        st.success("✅ Mot de passe changé avec succès !")
                    else:
                        st.error("❌ Mot de passe actuel incorrect")
        
        st.divider()
        
        st.subheader("Session active")
        st.info(f"Connecté depuis : {datetime.now().strftime('%d %B %Y à %H:%M')}")
        
        if st.button("🚪 Déconnecter tous les appareils", key="logout_all"):
            st.warning("Fonctionnalité à implémenter")
    
    # ============================================
    # ONGLET 3 : DONNÉES (avec données réelles)
    # ============================================
    with tab3:
        st.subheader("Gestion des données")
        
        # Statistiques RÉELLES
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Conversations", total_conversations)
        with col2:
            st.metric("Messages", total_messages)
        with col3:
            st.metric("Espace utilisé", f"{estimated_size:.1f} KB")
        
        st.divider()
        
        # Liste des conversations avec option de suppression individuelle
        st.subheader("Mes conversations")
        
        if not conversations:
            st.info("Vous n'avez pas encore de conversations")
        else:
            for conv in conversations:
                with st.container():
                    cols = st.columns([4, 1, 1])
                    
                    with cols[0]:
                        st.write(f"**{conv.get('name', 'Sans nom')}**")
                        st.caption(f"📅 {conv.get('created_at', '')[:10]}")
                    
                    with cols[1]:
                        # Compter les messages
                        msg_count = len(get_messages_by_conversation(conv['id']))
                        st.write(f"💬 {msg_count} messages")
                    
                    with cols[2]:
                        if st.button("🗑️", key=f"del_conv_{conv['id']}", help="Supprimer cette conversation"):
                            if delete_conversation(conv['id']):
                                st.success(f"✅ Conversation supprimée")
                                st.rerun()
                            else:
                                st.error("❌ Erreur lors de la suppression")
                    
                    st.divider()
        
        st.divider()
        
        # Actions globales
        st.warning("⚠️ Actions irréversibles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Exporter toutes mes données", key="export_data", use_container_width=True):
                st.info("Préparation de l'archive...")
                # Logique d'export à implémenter
        
        with col2:
            if st.button("🗑️ Supprimer toutes les conversations", key="delete_all_files", use_container_width=True):
                st.error("⚠️ Cette action supprimera TOUTES vos conversations !")
                confirm = st.checkbox("Je comprends que cette action est irréversible", key="confirm_all")
                
                if confirm:
                    if st.button("Confirmer la suppression totale", key="confirm_delete_all", type="primary"):
                        deleted_count = 0
                        for conv in conversations:
                            if delete_conversation(conv['id']):
                                deleted_count += 1
                        
                        if deleted_count > 0:
                            st.success(f"✅ {deleted_count} conversations supprimées")
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la suppression")
        
        st.divider()
        
        # Suppression du compte
        with st.expander("❌ Supprimer mon compte"):
            st.error("Cette action supprimera définitivement votre compte et TOUTES vos données.")
            
            confirm_delete = st.text_input(
                "Tapez 'SUPPRIMER' pour confirmer",
                key="confirm_delete_text"
            )
            
            if confirm_delete == "SUPPRIMER":
                if st.button("Supprimer définitivement mon compte", key="delete_account", type="primary"):
                    st.warning("Fonctionnalité à implémenter - Contactez le support")