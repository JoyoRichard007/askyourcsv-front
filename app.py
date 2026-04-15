import streamlit as st
import requests
import pandas as pd
import os
import plotly.io as pio
import streamlit.components.v1 as components
from dotenv import load_dotenv

# Configuration de la page
st.set_page_config(
    page_title="CSV Chat Playground",
    page_icon="🤖",
    layout="wide"
)

# Charger les variables d'environnement
load_dotenv()

# URL de base de l'API
API_BASE_URL = os.getenv("API_BASE_URL", "https://askyourcsv-production-b417.up.railway.app")

# Initialisation de la session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "process_id" not in st.session_state:
    st.session_state.process_id = None
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "provider" not in st.session_state:
    st.session_state.provider = "google"
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemini-3.1-flash-lite-preview"
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

# Fonction pour lire CSV avec différents encodages
def read_csv_with_encoding(file, encodings=['utf-8', 'latin1', 'cp1252']):
    for encoding in encodings:
        try:
            file.seek(0)
            df = pd.read_csv(file, encoding=encoding, nrows=5)  # Lire seulement 5 lignes pour l'aperçu
            return df, encoding
        except UnicodeDecodeError:
            continue
    file.seek(0)
    df = pd.read_csv(file, encoding='latin1', errors='replace', nrows=5)
    return df, 'latin1 (with replacements)'

# Interface principale
st.title("🤖 AskYourCSV")
st.markdown("Posez des questions en langage naturel sur vos fichiers CSV.")

# Sidebar - Configuration uniquement
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Fournisseur
    provider = st.selectbox(
        "Fournisseur",
        options=["google", "openai"],
        index=0,
        key="provider_select"
    )
    st.session_state.provider = provider
    
    # Clé API
    api_key = st.text_input(
        "Clé API",
        type="password",
        value=st.session_state.api_key,
        help=f"Entrez votre clé API {provider}",
        key="api_key_input"
    )
    if api_key:
        st.session_state.api_key = api_key
    
    # Modèle
    if provider == "google":
        models = ["gemini-3.1-flash-lite-preview", "gemini-3-flash-preview", "gemini-3.1-pro-preview"]
        default_model = "gemini-3.1-flash-lite-preview"
    else:
        models = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"]
        default_model = "gpt-4o-mini"
    
    model_name = st.selectbox(
        "Modèle",
        options=models,
        index=models.index(default_model) if default_model in models else 0,
        key="model_select"
    )
    st.session_state.model_name = model_name
    
    st.divider()
    
    # Upload de fichier
    st.header("📁 Fichier CSV")
    uploaded_file = st.file_uploader(
        "Choisissez un fichier",
        type="csv",
        key="csv_uploader"
    )
    
    if uploaded_file and st.session_state.api_key:
        if st.button("🚀 Upload", type="primary", use_container_width=True):
            with st.spinner("Upload en cours..."):
                try:
                    # Upload du fichier
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    params = {
                        "api_key": st.session_state.api_key,
                        "provider": st.session_state.provider
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/parquet/upload_file",
                        files=files,
                        params=params,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.process_id = data["file_id"]
                        st.session_state.uploaded_filename = uploaded_file.name
                        
                        # Lire un mini aperçu pour info
                        df, encoding = read_csv_with_encoding(uploaded_file)
                        st.session_state.df_info = {
                            "filename": uploaded_file.name,
                            "encoding": encoding,
                            "columns": list(df.columns),
                            "rows_preview": len(df),
                            "sample": df.head(3)
                        }
                        
                        st.success(f"✅ Fichier uploadé !")
                        st.rerun()
                    else:
                        st.error(f"❌ Erreur {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
    
    # Indicateur de session active
    if st.session_state.process_id:
        st.success("✅ Session active")
        if st.button("🔄 Nouvelle session", use_container_width=True):
            st.session_state.process_id = None
            st.session_state.messages = []
            st.session_state.uploaded_filename = None
            st.session_state.df_info = None
            st.rerun()
    
    st.divider()
    # st.caption(f"🔗 API: `{API_BASE_URL.split('//')[-1]}`")

# Zone de chat principale
if st.session_state.process_id and st.session_state.uploaded_filename:
    # Afficher le nom du fichier (optionnel)
    st.caption(f"📄 Fichier: {st.session_state.uploaded_filename}")
    
    # Afficher un mini aperçu dans un expander (optionnel)
    if hasattr(st.session_state, 'df_info') and st.session_state.df_info:
        with st.expander("📊 Aperçu rapide", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Colonnes:** {', '.join(st.session_state.df_info['columns'])}")
            with col2:
                st.write(f"**Encodage:** {st.session_state.df_info['encoding']}")
else:
    st.info("👈 Commencez par uploader un fichier CSV dans la sidebar")

# Chat
with st.container():
    # Afficher l'historique complet
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("chart_json"):
                fig = pio.from_json(message["chart_json"])
                st.plotly_chart(fig, use_container_width=True)

# Input toujours en bas
if prompt := st.chat_input("Posez votre question..."):
    if not st.session_state.api_key:
        st.error("⚠️ Veuillez d'abord entrer votre clé API")
        st.stop()
    if not st.session_state.process_id:
        st.error("⚠️ Veuillez d'abord uploader un fichier CSV")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Génération de la réponse si le dernier message est utilisateur
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    chart_keywords = [
        "graphique", "graph", "chart", "histogramme", "diagramme",
        "camembert", "pie chart", "barre", "courbe", "plot", "visualisation"
    ]
    is_chart_request = any(kw in last_prompt.lower() for kw in chart_keywords)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            try:
                if is_chart_request:
                    # Court-circuiter l'agent pour les graphiques -> appel direct /chart (plus rapide)
                    url = f"{API_BASE_URL}/chart/{st.session_state.process_id}"
                    payload = {
                        "prompt": last_prompt,
                        "api_key": st.session_state.api_key,
                        "provider": st.session_state.provider,
                        "model_name": st.session_state.model_name,
                    }
                    response = requests.post(url, json=payload, timeout=120)

                    if response.status_code == 200:
                        data = response.json()
                        chart_json = data["chart_json"]
                        assistant_msg = {
                            "role": "assistant",
                            "content": "Voici le graphique demandé :",
                            "chart_json": chart_json
                        }
                        st.markdown(assistant_msg["content"])
                        fig = pio.from_json(chart_json)
                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.messages.append(assistant_msg)
                        st.rerun()
                    else:
                        try:
                            err_detail = response.json().get("detail", response.text)
                        except Exception:
                            err_detail = response.text
                        st.error(f"❌ Erreur API : {err_detail}")
                else:
                    url = f"{API_BASE_URL}/askcsv/double/{st.session_state.process_id}"

                    messages_list = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages
                    ]

                    payload = {
                        "messages": messages_list,
                        "api_key": st.session_state.api_key,
                        "provider": st.session_state.provider,
                        "model_name": st.session_state.model_name
                    }

                    response = requests.post(url, json=payload, timeout=120)

                    if response.status_code == 200:
                        data = response.json()
                        assistant_message = data["messages"][0]["content"]
                        chart_json = data.get("chart_json")

                        # Message simplifié si time limit
                        if "Agent stopped due to iteration limit" in assistant_message:
                            assistant_message = "La question était complexe. Pouvez-vous la reformuler plus simplement ?"

                        st.markdown(assistant_message)
                        assistant_msg = {"role": "assistant", "content": assistant_message}
                        if chart_json:
                            fig = pio.from_json(chart_json)
                            st.plotly_chart(fig, use_container_width=True)
                            assistant_msg["chart_json"] = chart_json
                        st.session_state.messages.append(assistant_msg)
                        st.rerun()
                    else:
                        try:
                            err_detail = response.json().get("detail", response.text)
                        except Exception:
                            err_detail = response.text
                        st.error(f"❌ Erreur API : {err_detail}")

            except requests.exceptions.Timeout:
                st.warning("⚠️ Timeout - Question trop complexe")
                st.session_state.messages.append({"role": "assistant", "content": "⚠️ Timeout - Question trop complexe"})
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur")
                st.session_state.messages.append({"role": "assistant", "content": f"❌ Erreur"})
                st.rerun()

# Scroll auto vers le bas quand un nouveau message assistant arrive
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    components.html(
        """
        <script>
            try {
                window.parent.scrollTo({top: window.parent.document.documentElement.scrollHeight, behavior: 'smooth'});
            } catch(e) {}
        </script>
        """,
        height=0,
    )

# Bouton flottant pour scroller vers le bas (créé dynamiquement dans le DOM parent)
components.html(
    """
    <script>
    (function(){
        try {
            var parentDoc = window.parent.document;
            if (parentDoc.getElementById('kimi-scroll-btn')) return;
            var btn = parentDoc.createElement('div');
            btn.id = 'kimi-scroll-btn';
            btn.innerHTML = '↓';
            btn.style.cssText = 'position:fixed;bottom:80px;right:30px;width:45px;height:45px;border-radius:50%;background:#667eea;color:white;display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:999999;border:none;font-family:sans-serif;user-select:none;transition:transform 0.2s;';
            btn.addEventListener('mouseenter', function(){ btn.style.transform = 'scale(1.05)'; btn.style.background = '#5a6fd6'; });
            btn.addEventListener('mouseleave', function(){ btn.style.transform = 'scale(1)'; btn.style.background = '#667eea'; });
            btn.addEventListener('click', function(){
                window.parent.scrollTo({top: parentDoc.documentElement.scrollHeight, behavior: 'smooth'});
            });
            parentDoc.body.appendChild(btn);
        } catch(e) {}
    })();
    </script>
    """,
    height=0,
)

# Heartbeat pour maintenir le websocket actif sur Railway (évite le "Connecting...")
@st.fragment(run_every=2)
def _websocket_heartbeat():
    pass

_websocket_heartbeat()

# Footer minimal
st.divider()
st.caption("© Dimension")