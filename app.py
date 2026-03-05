# app.py
import streamlit as st
try:
    st.set_page_config(page_title="AskYourCSV", layout="wide")
except:
    # Si ça échoue (déjà configuré), on ignore
    pass
from PIL import Image
import time
from auth import sign_up, sign_in, sign_out 

# if not st.session_state.get("_page_config_set", False):
#     st.set_page_config(page_title="AskYourCSV", layout="wide")
#     st.session_state._page_config_set = True

# st.set_page_config(page_title="AskYourCSV", layout="wide")

# ----------------------------
# SESSION STATE
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:  
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "subpage" not in st.session_state:
    st.session_state.subpage = "csv_list"


# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

/* NAVBAR */
.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:20px 60px;
}

.logo {
    font-size:22px;
    font-weight:700;
    letter-spacing:3px;
}

/* Buttons */
.stButton>button {
    border-radius:8px;
    padding:8px 18px;
}

/* Step box */
.step-box {
    background-color:white;
    padding:18px;
    border-radius:12px;
    margin-bottom:12px;
    font-weight:500;
    display:flex;
    align-items:center;
    gap:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

/* Feature box */
.feature-box {
    background-color:white;
    padding:18px;
    border-radius:12px;
    margin-bottom:18px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

.feature-title {
    font-weight:600;
    margin-bottom:6px;
    color:#2563eb;
}

/* Dark button */
.dark-btn button {
    background-color:#1e293b !important;
    color:white !important;
}

.dark-btn button:hover {
    background-color:#0f172a !important;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------
# LANDING PAGE
# ----------------------------
def landing_page():
    # NAVBAR
    col_logo, col_space, col_btn = st.columns([6,2,2])

    with col_logo:
        st.markdown('<div class="logo">A s k Y o u r C S V</div>', unsafe_allow_html=True)

    with col_btn:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign In", key="landing_nav_signin"):
                st.session_state.page = "sign_in"
                st.rerun()
        with col2:
            if st.button("Sign Up", key="landing_nav_signup"):
                st.session_state.page = "sign_up"
                st.rerun()

    st.markdown("---")

    col1, col2 = st.columns(2)

    # LEFT
    with col1:
        st.markdown("# Master Your Data Effortlessly.")
        st.write("Managing and analyzing CSV files can be a daunting task, but it doesn’t have to be. Our platform is designed to make your data work for you. Whether you're a data analyst, a business owner, or just someone looking to simplify data management, we’ve got you covered.")

        st.markdown("""
        <div class="step-box">✅ Upload your CSV</div>
        <div class="step-box">✅ Ask your questions</div>
        <div class="step-box">✅ Get instant answers</div>
        """, unsafe_allow_html=True)

        st.write("Uncover trends, insights, and more with AskYourCSV's intuitive data analysis.")

        if st.button("Sign up to unlock your CSV potential", key="landing_cta_signup"):
            st.session_state.page = "sign_up"
            st.rerun()

        st.markdown("""
        <p style="margin-top:20px; opacity:0.7;">
        Join us today and unlock the full potential of your CSV data.
        </p>
        """, unsafe_allow_html=True)
    
    # RIGHT
    with col2:
        image = Image.open("assets/csv_landing.png")
        st.image(image, width=75)

        st.write("AskYourCSV lets you ask questions and get instant answers from your CSV files. Simplify the analysis of your data and obtain insights in just a few clicks.")
        st.write("Whether you're a marketer, financial analyst, researcher, or just someone working with data, AskYourCSV can help you unlock the full potential of your datasets. Here's how AskYourCSV can support your specific needs:")
        
        st.markdown("""
        <div class="feature-box">
            <div class="feature-title">⭐ Marketing</div>
            Analyze sales trends and customer behavior effortlessly.
        </div>

        <div class="feature-box">
            <div class="feature-title">⭐ Finance</div>
            Get precise financial statistics instantly.
        </div>

        <div class="feature-box">
            <div class="feature-title">⭐ Research</div>
            Easily interpret complex research data.
        </div>
        """, unsafe_allow_html=True)

        st.write("Learn about the file formats you can use with AskYourCSV to analyze and explore your data.")

# ----------------------------
# SIGN UP - Version corrigée (compacte)
# ----------------------------
def sign_up_page():
    # CSS ajusté pour moins de padding et formulaire compact
    st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
    }
    
    .auth-container {
        background: white;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        overflow: hidden;
        max-width: 1000px;
        margin: 20px auto;  /* Réduit de 40px à 20px */
    }
    
    .left-panel {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://miro.medium.com/v2/resize:fit:1400/0*B5SpyF1HLczosrES');
        background-size: cover;
        background-position: center;
        height: 100%;
        border-radius: 15px 0 0 15px;
        padding: 30px 25px;  /* Réduit de 40px à 30px */
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
    }
    
    /* Lien retour en haut à gauche */
    .back-link {
        position: absolute;
        top: 15px;
        left: 20px;
        color: white !important;
        text-decoration: none;
        font-size: 0.9rem;
        opacity: 0.9;
        cursor: pointer;
        background: rgba(255,255,255,0.2);
        padding: 5px 12px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        transition: all 0.2s ease;
    }
    
    .back-link:hover {
        opacity: 1;
        background: rgba(255,255,255,0.3);
        transform: translateX(-3px);
    }
    
    .left-panel h2 {
        color: white;
        font-weight: 700;
        margin: 30px 0 15px 0;  /* Ajusté pour le lien */
    }
    
    .left-panel ul {
        list-style: none;
        padding: 0;
        margin-bottom: 10px;
    }
    
    .left-panel li {
        margin: 10px 0;  /* Réduit de 15px à 10px */
        font-size: 1rem;  /* Réduit de 1.1rem à 1rem */
        display: flex;
        align-items: center;
    }
    
    .left-panel li:before {
        content: "✓";
        color: #4CAF50;
        font-weight: bold;
        margin-right: 10px;
        background: white;
        border-radius: 50%;
        padding: 2px 6px;
        font-size: 0.9rem;
    }
    
    .form-panel {
        background: white;
        padding: 25px 25px;  /* Réduit de 30px à 25px */
        height: 100%;
    }
    
    .form-panel h3 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.4rem;  /* Réduit de 1.5rem à 1.4rem */
        margin-bottom: 15px;  /* Réduit de 20px à 15px */
        text-align: center;
    }
    
    /* Champs plus compacts */
    .stTextInput > div > div > input {
        border-radius: 8px !important;  /* Réduit de 10px à 8px */
        border: 1px solid #e2e8f0 !important;
        padding: 6px 10px !important;  /* Réduit de 8px à 6px */
        font-size: 0.85rem !important;  /* Réduit de 0.9rem à 0.85rem */
        transition: all 0.2s ease !important;
    }
    
    /* Réduire l'espacement entre les champs */
    .row-widget {
        margin-bottom: 5px !important;  /* Réduit */
    }
    
    .stTextInput {
        margin-bottom: 5px !important;
    }
    
    .stButton > button {
        background: #10b981 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;  /* Réduit de 10px à 8px */
        padding: 8px 14px !important;  /* Réduit de 10px à 8px */
        font-weight: 500 !important;
        font-size: 0.9rem !important;  /* Réduit de 0.95rem à 0.9rem */
        width: 100% !important;
        transition: all 0.2s ease !important;
        margin: 5px 0 !important;  /* Réduit de 8px à 5px */
    }
    
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 10px 0;  /* Réduit de 15px à 10px */
        color: #94a3b8;
        font-size: 0.8rem;  /* Réduit de 0.85rem à 0.8rem */
    }
    
    .stAlert {
        border-radius: 6px !important;
        padding: 6px 10px !important;  /* Réduit */
        font-size: 0.8rem !important;  /* Réduit */
        margin: 5px 0 !important;
    }
    
    .stCheckbox {
        font-size: 0.8rem !important;  /* Réduit de 0.85rem à 0.8rem */
        margin: 3px 0 !important;
    }
    
    /* Ajuster la hauteur totale */
    .main > div {
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ✅ Conteneur principal
    st.markdown('<div style="max-width: 1000px; margin: 20px auto;">', unsafe_allow_html=True)
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # ✅ Deux colonnes principales
    left_col, right_col = st.columns([1, 1.2])
    
    # ===== PANNEAU GAUCHE =====
    with left_col:
        # Lien retour en haut (texte, pas bouton)
        st.markdown("""
        <div class="left-panel" style="position: relative;">
            <a class="back-link" onclick="window.location.href='?page=landing'">← Retour à l'accueil</a>
                    <h2>Rejoignez-nous</h2>
                    <div class="logo">A s k Y o u r C S V</div> <br/>
            <p style="font-size: 0.95rem; margin-bottom: 15px;">Commencez à analyser vos données CSV en quelques secondes.</p>
            <ul>
                <li>Fichiers CSV illimités</li>
                <li>Réponses instantanées par IA</li>
                <li>Insights puissants</li>
                <li>Stockage sécurisé</li>
                <li>100% gratuit pour démarrer</li>
            </ul>
            <h2 style="color : white">Des documents aux<br/>
conversations</h2>
            <p style="font-size: 1.75rem; margin-bottom: 15px;">
Connectez-vous et accédez à vos <br/>
données en quelques secondes</p>
        """, unsafe_allow_html=True)
        
        # Contenu du panneau
        st.markdown("""
            
        </div>
        """, unsafe_allow_html=True)
        
        # Plus de bouton ici, le lien est en haut
    
    # ===== FORMULAIRE DROIT =====
    with right_col:
        st.markdown("<h3>Inscription</h3>", unsafe_allow_html=True)
        
        # ✅ Prénom et Nom sur deux colonnes
        col_prenom, col_nom = st.columns(2)
        with col_prenom:
            first_name = st.text_input("Prénom", placeholder="Jean", key="signup_firstname")
        with col_nom:
            last_name = st.text_input("Nom", placeholder="Dupont", key="signup_lastname")
        
        # Autres champs
        username = st.text_input("Nom d'utilisateur", placeholder="jeandupont", key="signup_username")
        email = st.text_input("Email", placeholder="jean.dupont@email.com", key="signup_email")
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="signup_password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", placeholder="••••••••", key="signup_confirm")
        
        # Conditions
        terms = st.checkbox("J'accepte les conditions d'utilisation", key="terms")
        
        # Bouton d'inscription
        if st.button("Créer mon compte", key="signup_submit"):
            if not all([first_name, last_name, username, email, password, confirm_password]):
                st.error("❌ Veuillez remplir tous les champs")
            elif not terms:
                st.error("❌ Vous devez accepter les conditions")
            elif password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas")
            elif len(password) < 6:
                st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
            else:
                with st.spinner("Création en cours..."):
                    result = sign_up(email, password, first_name, last_name, username)
                    if result["success"]:
                        st.success("✅ Compte créé !")
                        st.session_state.logged_in = True
                        st.session_state.user = result["user"]
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
        
        # Séparateur
        st.markdown('<div class="divider"><span>ou</span></div>', unsafe_allow_html=True)
        
        # Lien vers connexion
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("Déjà un compte ?")
        if st.button("Se connecter", key="signup_to_signin", use_container_width=True):
            st.session_state.page = "sign_in"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------
# SIGN IN - Version corrigée (compacte)
# ----------------------------
def sign_in_page():
    # CSS ajusté
    st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
    }
    
    .auth-container {
        background: white;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        overflow: hidden;
        max-width: 900px;
        margin: 20px auto;
    }
    
    .left-panel {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://i.pinimg.com/736x/1a/13/5c/1a135caa588c42355610fd5b1502e43f.jpg');
        background-size: cover;
        background-position: center;
        height: 100%;
        border-radius: 15px 0 0 15px;
        padding: 30px 25px;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
    }
    
    .back-link {
        position: absolute;
        top: 15px;
        left: 20px;
        color: white !important;
        text-decoration: none;
        font-size: 0.9rem;
        opacity: 0.9;
        cursor: pointer;
        background: rgba(255,255,255,0.2);
        padding: 5px 12px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        transition: all 0.2s ease;
    }
    
    .back-link:hover {
        opacity: 1;
        background: rgba(255,255,255,0.3);
        transform: translateX(-3px);
    }
    
    .left-panel h2 {
        color: white;
        font-weight: 700;
        margin: 30px 0 15px 0;
    }
    
    .left-panel ul {
        list-style: none;
        padding: 0;
    }
    
    .left-panel li {
        margin: 8px 0;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
    }
    
    .left-panel li:before {
        content: "✓";
        color: #4CAF50;
        font-weight: bold;
        margin-right: 10px;
        background: white;
        border-radius: 50%;
        padding: 2px 6px;
        font-size: 0.9rem;
    }
    
    .form-panel {
        background: white;
        padding: 25px 25px;
        height: 100%;
    }
    
    .form-panel h3 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.4rem;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 6px 10px !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
    }
    
    .row-widget {
        margin-bottom: 5px !important;
    }
    
    .stTextInput {
        margin-bottom: 5px !important;
    }
    
    .stButton > button {
        background: #10b981 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        margin: 5px 0 !important;
    }
    
    .stButton > button:hover {
        background: #059669 !important;
        transform: translateY(-1px) !important;
    }
    
    .forgot-link button {
        background: transparent !important;
        color: #64748b !important;
        border: none !important;
        padding: 0 !important;
        font-size: 0.8rem !important;
        width: auto !important;
        margin: 0 !important;
    }
    
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 10px 0;
        color: #94a3b8;
        font-size: 0.8rem;
    }
    
    .stAlert {
        border-radius: 6px !important;
        padding: 6px 10px !important;
        font-size: 0.8rem !important;
        margin: 5px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ✅ Conteneur principal
    st.markdown('<div style="max-width: 900px; margin: 20px auto;">', unsafe_allow_html=True)
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # ✅ Deux colonnes principales
    left_col, right_col = st.columns(2)
    
    # ===== PANNEAU GAUCHE =====
    with left_col:
        st.markdown("""
        <div class="left-panel" style="position: relative;">
            <a class="back-link" onclick="window.location.href='?page=landing'">← Retour à l'accueil</a>
            <h2>Bon retour</h2>
            <p style="font-size: 0.95rem; margin-bottom: 15px;">Connectez-vous pour continuer votre analyse.</p>
            <ul>
                <li>Reprendre vos conversations</li>
                <li>Accéder à vos fichiers CSV</li>
                <li>Gérer vos paramètres</li>
                <li>Obtenir des insights personnalisés</li>
            </ul>
            <h3 style="color : white">Des documents aux<br/>
conversations</h3>
            <p style="font-size: 1.75rem; margin-bottom: 15px;">
Créez un compte en 2 minutes et rejoignez-nous <br/>
pour un accès complet</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== FORMULAIRE DROIT =====
    with right_col:
        st.markdown("<br/><h3>Connexion</h3>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="jean.dupont@email.com", key="signin_email")
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="signin_password")
        
        # Options
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            remember = st.checkbox("Se souvenir de moi", key="remember_me")
        # with opt_col2:
        #     st.markdown('<div class="forgot-link" style="text-align: right;">', unsafe_allow_html=True)
        #     if st.button("Mot de passe oublié ?", key="signin_forgot"):
        #         st.info("Contactez le support pour réinitialiser votre mot de passe.")
        #     st.markdown('</div>', unsafe_allow_html=True)
        
        # Bouton de connexion
        if st.button("Se connecter", key="signin_submit"):
            if not email or not password:
                st.error("❌ Veuillez remplir tous les champs")
            else:
                with st.spinner("Connexion en cours..."):
                    result = sign_in(email, password)
                    if result["success"]:
                        st.success("✅ Connexion réussie !")
                        st.session_state.logged_in = True
                        st.session_state.user = result["user"]
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(f"❌ {result['error']}")
        
        # Séparateur
        st.markdown('<div class="divider"><span>ou</span></div>', unsafe_allow_html=True)
        
        # Lien vers inscription
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("Pas encore de compte ?")
        if st.button("Créer un compte", key="signin_to_signup", use_container_width=True):
            st.session_state.page = "sign_up"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------
# ROUTER UNIQUE
# ----------------------------
# Si l'utilisateur est déjà connecté et essaie d'accéder aux pages publiques
if st.session_state.logged_in:
    # Rediriger vers le dashboard
    if st.session_state.page in ["landing", "sign_in", "sign_up"]:
        st.session_state.page = "dashboard"
        st.rerun()
    
    # Pages privées - importées du dossier page/
    if st.session_state.page == "dashboard":
        from page.dashboard import show
        show()
    elif st.session_state.page == "csv_list":
        from page.csv_list import show
        show()
    elif st.session_state.page == "import_csv":
        from page.import_csv import show
        show()
    elif st.session_state.page == "conversation":
        from page.conversation import show
        show()
    elif st.session_state.page == "settings":
        from page.settings import show
        show()
    else:
        # Par défaut
        from page.dashboard import show
        show()

else:
    # Utilisateur NON connecté - pages publiques
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "sign_up":
        sign_up_page()
    elif st.session_state.page == "sign_in":
        sign_in_page()
    else:
        # Si une page privée est demandée sans être connecté
        st.session_state.page = "landing"
        st.rerun()