# page/sidebar.py
import streamlit as st

def show_sidebar(current_page):
    """Affiche la sidebar avec des clés uniques basées sur la page courante"""
    
    with st.sidebar:
        if st.session_state.user:
            first_name = st.session_state.user.get('first_name', '')
            last_name = st.session_state.user.get('last_name', '')
            email = st.session_state.user.get('email', '')
            initial = first_name[0] if first_name else email[0].upper()
            
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            width: 80px; height: 80px; border-radius: 50%; 
                            margin: 0 auto 10px auto; display: flex; 
                            align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 32px; font-weight: bold;">
                        {initial}
                    </span>
                </div>
                <div style="font-weight: bold;">{first_name} {last_name}</div>
                <div style="font-size: 0.8rem; color: #666;">{email}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.sidebar.title("Menu")
        
        # Définition des items du menu
        menu_items = [
            ("📊 Dashboard", "dashboard"),
            ("📁 CSV List", "csv_list"),
            ("📤 Import CSV", "import_csv"),
            # ("💬 Messages", "conversation"),
            ("⚙️ Settings", "settings"),
        ]
        
        # Créer des clés uniques basées sur la page courante
        for label, page in menu_items:
            # Clé unique = page_source + destination
            key = f"{current_page}_to_{page}"
            
            if st.sidebar.button(label, key=key, use_container_width=True):
                st.session_state.page = page
                st.rerun()
        
        st.sidebar.divider()
        
        # Logout avec clé unique aussi
        logout_key = f"{current_page}_logout"
        if st.sidebar.button("🚪 Log Out", key=logout_key, use_container_width=True, type="primary"):
            from auth import sign_out
            sign_out()
            st.rerun()