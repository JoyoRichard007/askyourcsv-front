# page/import_csv.py - Version avec seulement la réponse enregistrée
import streamlit as st
import pandas as pd
from page.sidebar import show_sidebar
from api import upload_csv_file, ask_csv
from database import create_conversation, add_message
import time

def show():
    """Page d'import CSV"""
    
    show_sidebar("import_csv")
    
    st.title("📤 Import CSV")
    st.markdown("Chargez votre fichier CSV pour commencer l'analyse")
    
    with st.expander("ℹ️ Format du fichier attendu"):
        st.markdown("""
        - Fichier **CSV** avec encodage **Latin1 (ISO-8859-1)**
        - Première ligne = en-têtes de colonnes
        - Pas de limite de taille
        """)
    
    uploaded_file = st.file_uploader(
        "Choisissez un fichier CSV", 
        type=["csv"],
        key="import_file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            # Aperçu avec latin1
            uploaded_file.seek(0)
            df_preview = pd.read_csv(uploaded_file, encoding='latin1', nrows=5)
            uploaded_file.seek(0)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"✅ Fichier chargé : **{uploaded_file.name}**")
                st.write(f"📊 Taille : **{uploaded_file.size / 1024:.2f} KB**")
                st.write(f"📋 Colonnes : **{len(df_preview.columns)}**")
            
            with col2:
                st.info("Aperçu des 5 premières lignes")
                st.dataframe(df_preview, use_container_width=True)
            
            st.divider()
            
            conversation_name = st.text_input(
                "Nom de la conversation (optionnel)",
                placeholder=uploaded_file.name.replace('.csv', ''),
                key="conv_name"
            )
            
            if st.button("🚀 Importer et analyser", key="confirm_import", use_container_width=True):
                with st.spinner("Upload du fichier en cours..."):
                    # 1. Upload vers FastAPI
                    uploaded_file.seek(0)
                    api_result = upload_csv_file(uploaded_file)
                    
                    if api_result:
                        file_id = api_result.get("file_id")
                        detected_separator = api_result.get("separator", ";")
                        
                        # 2. Créer la conversation
                        conv_name = conversation_name or uploaded_file.name.replace('.csv', '')
                        conv_result = create_conversation(
                            user_id=st.session_state.user.get('id'),
                            file_id=file_id,
                            file_name=uploaded_file.name,
                            separator=detected_separator,
                            name=conv_name
                        )
                        
                        if conv_result["success"]:
                            conversation_id = conv_result["conversation"]["id"]
                            
                            # 3. 🇫🇷 GÉNÉRER LA RÉPONSE SANS ENREGISTRER LA QUESTION
                            with st.spinner("Génération du résumé des données..."):
                                
                                # Appeler l'API directement avec la question (sans l'enregistrer)
                                api_messages = [{"role": "human", "content": "Que contient le dataframe ?"}]
                                result = ask_csv(file_id, api_messages)
                                
                                if result and "messages" in result:
                                    assistant_response = result["messages"][-1]["content"]
                                    # ✅ Enregistrer SEULEMENT la réponse comme premier message
                                    add_message(conversation_id, "assistant", assistant_response, 0)
                                    st.success("✅ Résumé généré automatiquement !")
                                else:
                                    # Message par défaut si l'API échoue
                                    default_response = "Le dataframe a été chargé avec succès. Vous pouvez maintenant poser des questions sur les données."
                                    add_message(conversation_id, "assistant", default_response, 0)
                                    st.warning("⚠️ Résumé automatique non disponible")
                            
                            # 4. Rediriger vers la conversation
                            st.session_state.current_conversation = conversation_id
                            st.session_state.page = "conversation"
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ Erreur création conversation: {conv_result.get('error')}")
                    else:
                        st.error("❌ Erreur lors de l'upload")
        
        except Exception as e:
            st.error(f"❌ Erreur : {e}")