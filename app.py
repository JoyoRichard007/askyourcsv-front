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

# =============================================================================
# CSS GLOBAL — Thème dark moderne inspiré de Dashboard.html
# =============================================================================
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Hide Streamlit chrome */
[data-testid="stHeader"] {display: none !important;}
[data-testid="stFooter"] {display: none !important;}
[data-testid="stMainMenu"] {display: none !important;}
#MainMenu {display: none !important;}

/* Ensure sidebar collapsed control stays above custom nav */
[data-testid="stSidebarCollapsedControl"] {
  z-index: 999999 !important;
}

:root {
  --ay-bg: #16181f;
  --ay-panel: #1f222a;
  --ay-panel-2: #23262f;
  --ay-panel-deep: #1a1c23;
  --ay-line: #2f333d;
  --ay-line-2: #404550;
  --ay-ink: #f0f1f5;
  --ay-ink-2: #c5c9d3;
  --ay-ink-3: #8a8f9d;
  --ay-accent: #9ef08a;
  --ay-accent-ink: #1f3a1a;
  --ay-cyan: #7ecce0;
  --ay-user-bubble: rgba(158, 240, 138, 0.10);
  --ay-user-bubble-border: rgba(158, 240, 138, 0.35);
  --ay-sidebar-bg: #13151b;
  --ay-sans: 'Inter', system-ui, sans-serif;
  --ay-mono: 'JetBrains Mono', ui-monospace, monospace;
}

/* App shell */
[data-testid="stAppViewContainer"] {
  background: var(--ay-bg);
  color: var(--ay-ink);
  font-family: var(--ay-sans);
}
[data-testid="stAppViewContainer"] .main {
  background: var(--ay-bg);
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: var(--ay-sidebar-bg) !important;
  border-right: 1px solid var(--ay-line) !important;
}
[data-testid="stSidebarContent"] {
  background: transparent !important;
}
section[data-testid="stSidebar"] .block-container {
  padding-top: 1rem !important;
  padding-bottom: 1rem !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--ay-sans) !important;
  color: var(--ay-ink) !important;
  letter-spacing: -0.01em !important;
}
p, li, div, span {
  font-family: var(--ay-sans);
  color: var(--ay-ink-2);
}

/* Sidebar section headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: var(--ay-mono) !important;
  font-size: 12.5px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  color: var(--ay-ink) !important;
  margin-bottom: 0.5rem !important;
}

/* Form labels */
[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label,
[data-testid="stFileUploader"] label,
[data-testid="stChatInput"] label {
  color: var(--ay-ink-2) !important;
  font-family: var(--ay-mono) !important;
  font-size: 11.5px !important;
}

/* Inputs & selects */
[data-testid="stSelectbox"] > div[data-baseweb="select"] > div,
[data-testid="stTextInput"] > div > div,
[data-testid="stFileUploader"] > section > div > div,
[data-testid="stChatInput"] > div > div {
  background: var(--ay-panel) !important;
  border: 1px solid var(--ay-line) !important;
  border-radius: 10px !important;
  color: var(--ay-ink) !important;
}
[data-testid="stSelectbox"] span {
  color: var(--ay-ink) !important;
}

/* File uploader drag zone */
[data-testid="stFileUploader"] section {
  background: var(--ay-panel) !important;
  border: 1.5px dashed var(--ay-line-2) !important;
  border-radius: 14px !important;
}
[data-testid="stFileUploader"] section:hover {
  border-color: var(--ay-accent) !important;
  background: rgba(158, 240, 138, 0.05) !important;
}
[data-testid="stFileUploader"] section *,
[data-testid="stFileUploader"] section p,
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section div,
[data-testid="stFileUploader"] section small,
[data-testid="stFileUploader"] section button {
  color: var(--ay-ink) !important;
}

/* File uploader button */
[data-testid="stFileUploader"] button {
  background: var(--ay-panel-2) !important;
  color: var(--ay-ink) !important;
  border: 1px solid var(--ay-line-2) !important;
  border-radius: 8px !important;
  font-family: var(--ay-mono) !important;
  font-size: 11px !important;
  font-weight: 500 !important;
}
[data-testid="stFileUploader"] button:hover {
  background: var(--ay-panel) !important;
  border-color: var(--ay-accent) !important;
  color: var(--ay-ink) !important;
}

/* Buttons */
.stButton > button {
  font-family: var(--ay-mono) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  background: var(--ay-panel) !important;
  color: var(--ay-ink) !important;
  border: 1px solid var(--ay-line-2) !important;
  border-radius: 8px !important;
  transition: background .15s, border-color .15s, color .15s !important;
}
.stButton > button:hover {
  background: var(--ay-panel-2) !important;
  border-color: var(--ay-ink-3) !important;
  color: var(--ay-ink) !important;
}
.stButton > button[kind="primary"] {
  background: var(--ay-accent) !important;
  color: #000 !important;
  border-color: transparent !important;
  box-shadow: 0 0 0 1px rgba(158, 240, 138, 0.4), 0 8px 24px -10px rgba(158, 240, 138, 0.6) !important;
  font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
  filter: brightness(1.06) !important;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
  background: transparent !important;
}
[data-testid="stChatMessageAvatar"] {
  border-radius: 8px !important;
  border: 1px solid var(--ay-line-2) !important;
  overflow: hidden !important;
}
[data-testid="stChatMessageContent"] {
  background: var(--ay-panel) !important;
  border: 1px solid var(--ay-line) !important;
  border-radius: 14px !important;
  padding: 14px 16px !important;
  color: var(--ay-ink) !important;
  font-size: 14.5px !important;
  line-height: 1.55 !important;
}
/* User bubble: avatar is the last child in row-reverse layout */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatar"]:last-child) [data-testid="stChatMessageContent"] {
  background: var(--ay-user-bubble) !important;
  border-color: var(--ay-user-bubble-border) !important;
}

/* Chat input */
[data-testid="stChatInput"] {
  background: var(--ay-panel) !important;
  border: 1px solid var(--ay-line-2) !important;
  border-radius: 14px !important;
  box-shadow: 0 10px 40px -20px rgba(0,0,0,0.4) !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--ay-accent) !important;
  box-shadow: 0 0 0 3px rgba(158, 240, 138, 0.15), 0 10px 40px -20px rgba(0,0,0,0.4) !important;
}
[data-testid="stChatInput"] textarea {
  background: transparent !important;
  color: var(--ay-ink) !important;
  font-family: var(--ay-sans) !important;
  font-size: 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: var(--ay-ink-3) !important;
}

/* Expander */
[data-testid="stExpander"] {
  border: 1px solid var(--ay-line) !important;
  border-radius: 12px !important;
  background: var(--ay-panel) !important;
  overflow: hidden !important;
}
[data-testid="stExpander"] summary {
  font-family: var(--ay-mono) !important;
  font-size: 12px !important;
  color: var(--ay-ink-2) !important;
  background: var(--ay-panel) !important;
  padding: 10px 14px !important;
}
[data-testid="stExpander"] summary:hover {
  color: var(--ay-ink) !important;
}
[data-testid="stExpander"] .streamlit-expanderContent {
  background: var(--ay-panel) !important;
  color: var(--ay-ink-2) !important;
}

/* Alerts (info, success, error, warning) */
[data-testid="stAlert"] {
  background: var(--ay-panel) !important;
  border: 1px solid var(--ay-line) !important;
  border-radius: 10px !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
  color: var(--ay-ink) !important;
}

/* Spinner */
[data-testid="stSpinner"] > div {
  border-color: var(--ay-accent) !important;
  border-top-color: transparent !important;
}
[data-testid="stSpinner"] > div + div {
  color: var(--ay-ink-2) !important;
  font-family: var(--ay-mono) !important;
  font-size: 12px !important;
}

/* Captions */
[data-testid="stCaptionContainer"] {
  color: var(--ay-ink-3) !important;
  font-family: var(--ay-mono) !important;
  font-size: 11px !important;
}

/* Dividers */
hr {
  border-color: var(--ay-line) !important;
  margin: 1rem 0 !important;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: var(--ay-bg);
}
::-webkit-scrollbar-thumb {
  background: var(--ay-line);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--ay-line-2);
}

/* Custom top nav */
.custom-nav {
    position: sticky; top: 0; z-index: 50;
    backdrop-filter: blur(10px);
    background: rgba(22,24,31,0.85);
    border-bottom: 1px solid var(--ay-line);
    padding: 0 22px;
    height: 56px;
    display: flex; align-items: center; justify-content: space-between;
    margin: -1rem -1rem 1rem -1rem;
    width: calc(100% + 2rem);
}
.custom-nav .brand {
    display: flex; align-items: center; gap: 10px;
    font-family: var(--ay-mono); font-weight: 600; letter-spacing: -0.01em;
    color: var(--ay-ink); text-decoration: none;
}
.custom-nav .brand-mark {
    width: 22px; height: 22px; border-radius: 5px;
    background: linear-gradient(135deg, var(--ay-accent), #7dd868);
    box-shadow: 0 0 0 1px var(--ay-line-2), inset 0 1px 0 rgba(255,255,255,0.3);
    display: grid; place-items: center;
    color: var(--ay-accent-ink); font-size: 11px;
}
.custom-nav .nav-links {
    display: flex; gap: 18px; align-items: center;
    font-family: var(--ay-mono); font-size: 13px; color: var(--ay-ink-2);
}
.custom-nav .nav-links a {
    color: inherit; text-decoration: none;
}
.custom-nav .nav-links a:hover { color: var(--ay-ink); }

/* Scroll-to-bottom button override */
.scroll-btn {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(158, 240, 138, 0.55);
    color: var(--ay-accent-ink) !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    text-decoration: none;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    z-index: 999999;
    border: none;
    font-family: var(--ay-mono);
    opacity: 0.85;
    transition: opacity 0.15s, transform 0.15s, background 0.15s;
}
.scroll-btn:hover {
    background: rgba(158, 240, 138, 0.9);
    opacity: 1;
    transform: scale(1.05);
}
</style>
""")

# Header / Nav custom
st.html("""
<div class="custom-nav">
    <a class="brand" href="https://askyourcsv-production.up.railway.app" target="_self">
        <div class="brand-mark">▤</div>
        askyourcsv<span style="color:var(--ay-accent)">.</span>
    </a>
    <div class="nav-links">
        <a href="https://askyourcsv-production.up.railway.app" target="_self">Accueil</a>
        <a href="https://t.me/askyourcsv_bot" target="_blank">Telegram</a>
    </div>
</div>
""")

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
            df = pd.read_csv(file, encoding=encoding, nrows=6)  # Lire 6 lignes pour l'aperçu
            return df, encoding
        except UnicodeDecodeError:
            continue
    file.seek(0)
    df = pd.read_csv(file, encoding='latin1', errors='replace', nrows=6)
    return df, 'latin1 (with replacements)'

# Interface principale
st.html("""
<div style="max-width:860px;margin:0 0 4px 0;width:100%;display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap">
    <div>
        <h1 style="margin:0;font-size:22px;font-weight:600;letter-spacing:-0.015em;color:var(--ay-ink)">AskYourCSV</h1>
        <div style="font-family:var(--ay-mono);font-size:10.5px;color:var(--ay-ink-3);margin-top:4px">Posez des questions en langage naturel sur vos fichiers CSV.</div>
    </div>
</div>
""")

# Sidebar - Configuration uniquement
with st.sidebar:
    st.html('<div style="font-family:var(--ay-mono);font-size:10.5px;color:var(--ay-ink-3);letter-spacing:0.08em;text-transform:uppercase;padding:10px 0 4px;font-weight:600">Configuration</div>')
    
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
    st.html('<div style="font-family:var(--ay-mono);font-size:10.5px;color:var(--ay-ink-3);letter-spacing:0.08em;text-transform:uppercase;padding:10px 0 4px;font-weight:600">Fichier CSV</div>')
    uploaded_file = st.file_uploader(
        "Choisissez un fichier",
        type="csv",
        key="csv_uploader"
    )
    
    if uploaded_file and st.session_state.api_key:
        if st.button("Upload", use_container_width=True):
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
                            "sample": df.head(6)
                        }
                        
                        st.success("Fichier uploadé !")
                        st.rerun()
                    else:
                        st.error(f"❌ Erreur {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
    
    # Indicateur de session active
    if st.session_state.process_id:
        st.html('<div style="text-align:center;padding:10px 14px;border-radius:10px;border:1px solid rgba(158,240,138,0.35);background:rgba(158,240,138,0.10);color:var(--ay-accent);font-family:var(--ay-mono);font-size:12px;font-weight:500;margin-bottom:10px">Session active</div>')
        if st.button("Nouvelle session", use_container_width=True):
            st.session_state.process_id = None
            st.session_state.messages = []
            st.session_state.uploaded_filename = None
            st.session_state.df_info = None
            st.rerun()
    
    st.divider()
    # st.caption(f"🔗 API: `{API_BASE_URL.split('//')[-1]}`")

# Zone de chat principale
if st.session_state.process_id and st.session_state.uploaded_filename:
    # File pill (style Dashboard.html)
    st.html(f"""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">
        <span style="display:inline-flex;align-items:center;gap:8px;padding:7px 10px 7px 8px;border:1px solid var(--ay-line);border-radius:10px;background:var(--ay-panel);font-family:var(--ay-mono);font-size:12px;color:var(--ay-ink-2)">
            <span style="width:7px;height:7px;border-radius:50%;background:var(--ay-accent);display:inline-block"></span>
            {st.session_state.uploaded_filename}
            <span style="color:var(--ay-ink-3);font-size:10.5px;margin-left:4px">active</span>
        </span>
    </div>
    """)
    
    # Afficher un mini aperçu dans un expander
    if hasattr(st.session_state, 'df_info') and st.session_state.df_info:
        with st.expander("Aperçu rapide", expanded=False):
            st.caption(f"{st.session_state.df_info['rows_preview']} lignes · {len(st.session_state.df_info['columns'])} colonnes · {st.session_state.df_info['encoding']}")
            st.dataframe(st.session_state.df_info['sample'], use_container_width=True, hide_index=True)
else:
    st.info("← Commencez par uploader un fichier CSV dans la sidebar")

# Chat
with st.container():
    # Afficher l'historique complet
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("chart_json"):
                fig = pio.from_json(message["chart_json"])
                st.plotly_chart(fig, use_container_width=True)

# Suggestions (style Dashboard.html)
if st.session_state.process_id and not (st.session_state.messages and st.session_state.messages[-1]["role"] == "user"):
    SUGGESTIONS = [
        "Quels sont les 5 premiers enregistrements ?",
        "Montre-moi un graphique des données",
        "Résume les colonnes et les statistiques",
        "Quelles sont les valeurs uniques ?"
    ]
    st.html('<div style="font-family:var(--ay-mono);font-size:11px;color:var(--ay-ink-3);margin-bottom:6px">try asking</div>')
    sug_cols = st.columns(len(SUGGESTIONS))
    for i, sug in enumerate(SUGGESTIONS):
        if sug_cols[i].button(sug, key=f"sug_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": sug})
            st.rerun()

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

# Ancre pour scroll en bas (sera la cible du lien)
if "bottom_anchor" not in st.session_state:
    st.session_state.bottom_anchor = True

# Bouton flottant lien HTML natif (pas de JS)
st.html("""
<style>
.scroll-btn {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(158, 240, 138, 0.55);
    color: #1f3a1a !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    text-decoration: none;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    z-index: 999999;
    border: none;
    font-family: sans-serif;
    opacity: 0.85;
    transition: opacity 0.15s, transform 0.15s, background 0.15s;
}
.scroll-btn:hover {
    background: rgba(158, 240, 138, 0.9);
    opacity: 1;
    transform: scale(1.05);
}
</style>
<a href="#bottom-anchor" class="scroll-btn">↓</a>
""")

# Heartbeat pour maintenir le websocket actif sur Railway (évite le "Connecting...")
@st.fragment(run_every=2)
def _websocket_heartbeat():
    pass

_websocket_heartbeat()

# Footer minimal
st.divider()
st.caption("© Dimension")

# Ancre finale pour le scroll vers le bas
st.html('<div id="bottom-anchor" style="height:0px;"></div>')
