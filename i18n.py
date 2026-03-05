# i18n.py
import streamlit as st

# Dictionnaire des traductions
TRANSLATIONS = {
    'fr': {
        # Questions automatiques
        'auto_question': "Que contient le dataframe ?",
        'default_response': "Le dataframe a été chargé avec succès. Vous pouvez maintenant poser des questions sur les données.",
        
        # Interface générale
        'welcome': "Bienvenue",
        'dashboard': "Tableau de bord",
        'csv_list': "Liste CSV",
        'import_csv': "Importer CSV",
        'conversations': "Conversations",
        'settings': "Paramètres",
        'logout': "Déconnexion",
        
        # Import CSV
        'upload_title': "📤 Import CSV",
        'upload_description': "Chargez votre fichier CSV pour commencer l'analyse",
        'file_loaded': "Fichier chargé",
        'columns_detected': "Colonnes détectées",
        'preview': "Aperçu des 5 premières lignes",
        'conversation_name': "Nom de la conversation (optionnel)",
        'import_button': "🚀 Importer et analyser",
        
        # Conversation
        'ask_question': "Posez votre question sur les données...",
        'back': "← Retour",
        'new_conversation': "Nouvelle conversation",
        'delete': "Supprimer",
        'open': "Ouvrir",
        
        # Messages d'erreur
        'error_upload': "Erreur lors de l'upload",
        'error_api': "Erreur lors de l'analyse",
        'error_process_id': "ID de processus non trouvé",
    },
    'en': {
        # Auto questions
        'auto_question': "What does the dataframe contain?",
        'default_response': "The dataframe has been loaded successfully. You can now ask questions about the data.",
        
        # General UI
        'welcome': "Welcome",
        'dashboard': "Dashboard",
        'csv_list': "CSV List",
        'import_csv': "Import CSV",
        'conversations': "Conversations",
        'settings': "Settings",
        'logout': "Logout",
        
        # Import CSV
        'upload_title': "📤 Import CSV",
        'upload_description': "Upload your CSV file to start analyzing",
        'file_loaded': "File loaded",
        'columns_detected': "Columns detected",
        'preview': "Preview of first 5 rows",
        'conversation_name': "Conversation name (optional)",
        'import_button': "🚀 Import and analyze",
        
        # Conversation
        'ask_question': "Ask a question about your data...",
        'back': "← Back",
        'new_conversation': "New conversation",
        'delete': "Delete",
        'open': "Open",
        
        # Error messages
        'error_upload': "Upload error",
        'error_api': "Analysis error",
        'error_process_id': "Process ID not found",
    },
    'es': {
        'auto_question': "¿Qué contiene el dataframe?",
        'default_response': "El dataframe se ha cargado correctamente. Ahora puedes hacer preguntas sobre los datos.",
        'welcome': "Bienvenido",
        'dashboard': "Panel",
        'csv_list': "Lista CSV",
        'import_csv': "Importar CSV",
        'conversations': "Conversaciones",
        'settings': "Ajustes",
        'logout': "Cerrar sesión",
        'upload_title': "📤 Importar CSV",
        'upload_description': "Carga tu archivo CSV para comenzar el análisis",
        'file_loaded': "Archivo cargado",
        'columns_detected': "Columnas detectadas",
        'preview': "Vista previa de las 5 primeras filas",
        'conversation_name': "Nombre de la conversación (opcional)",
        'import_button': "🚀 Importar y analizar",
        'ask_question': "Haz una pregunta sobre tus datos...",
        'back': "← Volver",
        'new_conversation': "Nueva conversación",
    }
}

def t(key):
    """Fonction de traduction simple"""
    lang = st.session_state.get('language', 'fr')
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)

def language_selector():
    """Affiche un sélecteur de langue dans la sidebar"""
    with st.sidebar:
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🇫🇷 FR", key="lang_fr", 
                        use_container_width=True,
                        type="primary" if st.session_state.language == 'fr' else "secondary"):
                st.session_state.language = 'fr'
                st.rerun()
        with col2:
            if st.button("🇬🇧 EN", key="lang_en",
                        use_container_width=True,
                        type="primary" if st.session_state.language == 'en' else "secondary"):
                st.session_state.language = 'en'
                st.rerun()
        with col3:
            if st.button("🇪🇸 ES", key="lang_es",
                        use_container_width=True,
                        type="primary" if st.session_state.language == 'es' else "secondary"):
                st.session_state.language = 'es'
                st.rerun()