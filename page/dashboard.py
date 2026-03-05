# page/dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from page.sidebar import show_sidebar
from database import get_user_conversations, get_messages_by_conversation
import plotly.graph_objects as go

def show():
    """Dashboard principal avec données réelles uniquement"""
    
    show_sidebar("dashboard")
    
    # Récupérer les données réelles de l'utilisateur
    user_id = st.session_state.user.get('id')
    conversations = get_user_conversations(user_id)
    
    # ============================================
    # CALCUL DES STATISTIQUES RÉELLES UNIQUEMENT
    # ============================================
    
    total_conversations = len(conversations)
    total_messages = 0
    messages_par_jour = {}
    
    for conv in conversations:
        # Compter les messages
        messages = get_messages_by_conversation(conv['id'])
        total_messages += len(messages)
        
        # Compter les messages par jour
        for msg in messages:
            msg_date = msg.get('created_at', '')[:10]
            if msg_date:
                messages_par_jour[msg_date] = messages_par_jour.get(msg_date, 0) + 1
    
    # Dernière activité
    last_activity = "Aucune activité"
    if conversations:
        last_conv_date = max([c.get('created_at', '') for c in conversations if c.get('created_at')])
        if last_conv_date:
            last_activity = last_conv_date[:16].replace('T', ' ')
    
    # ============================================
    # EN-TÊTE
    # ============================================
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Dashboard")
        if st.session_state.user:
            welcome_name = st.session_state.user.get('first_name', '') or st.session_state.user.get('email', '')
            st.markdown(f"### 👋 Bon retour parmi nous, **{welcome_name}** !")
    
    with col2:
        st.markdown(f"""
        <div style="text-align: right; padding: 20px 0;">
            <div style="font-size: 0.9rem; color: #666;">{datetime.now().strftime('%d %B %Y')}</div>
            <div style="font-size: 0.8rem; color: #999;">Dernière activité: {last_activity}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ============================================
    # STATISTIQUES RAPIDES (uniquement données réelles)
    # ============================================
    st.subheader("📈 Aperçu rapide")
    
    col1, col2, col3 = st.columns(3)  # Passé de 4 à 3 colonnes (supprimé satisfaction)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <div style="font-size: 2rem; font-weight: bold;">{total_conversations}</div>
            <div style="font-size: 0.9rem;">Conversations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <div style="font-size: 2rem; font-weight: bold;">{total_messages}</div>
            <div style="font-size: 0.9rem;">Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Moyenne messages par conversation (donnée réelle calculée)
        avg_messages = round(total_messages / total_conversations, 1) if total_conversations > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <div style="font-size: 2rem; font-weight: bold;">{avg_messages}</div>
            <div style="font-size: 0.9rem;">Moy. messages/conv</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ============================================
    # ACTIVITÉ RÉCENTE
    # ============================================
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Activité récente")
        
        if not conversations:
            st.info("Aucune activité récente")
        else:
            # Préparer les activités récentes (5 dernières)
            recent_activities = []
            for conv in conversations[:5]:
                messages = get_messages_by_conversation(conv['id'])
                if messages:
                    last_msg = messages[-1]
                    recent_activities.append({
                        "action": "💬 Message",
                        "item": conv.get('name', 'Sans nom')[:30],
                        "time": last_msg.get('created_at', '')[:16].replace('T', ' '),
                        "status": "✅ Réponse"
                    })
                else:
                    recent_activities.append({
                        "action": "📤 Import",
                        "item": conv.get('name', 'Sans nom')[:30],
                        "time": conv.get('created_at', '')[:16].replace('T', ' '),
                        "status": "⏳ En attente"
                    })
            
            for activity in recent_activities:
                with st.container():
                    cols = st.columns([2, 2, 2, 1])
                    with cols[0]:
                        st.write(f"**{activity['action']}**")
                    with cols[1]:
                        st.write(activity['item'])
                    with cols[2]:
                        st.write(activity['time'])
                    with cols[3]:
                        st.write(activity['status'])
                    st.divider()
    
    with col2:
        st.subheader("📊 Activité par jour")
        
        if messages_par_jour:
            # Trier les dates
            dates_sorted = sorted(messages_par_jour.keys())
            values = [messages_par_jour[date] for date in dates_sorted]
            
            # Graphique avec Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates_sorted,
                y=values,
                mode='lines+markers',
                name='Messages',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="Évolution des messages",
                xaxis_title="Date",
                yaxis_title="Nombre de messages",
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Stats du jour (données réelles)
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Jours avec activité", len(messages_par_jour))
            with col_stat2:
                if dates_sorted:
                    dernier_jour = dates_sorted[-1]
                    st.metric("Dernier message", dernier_jour)
        else:
            st.info("Aucune activité à afficher")
            fig = go.Figure()
            fig.update_layout(
                height=300,
                title="Pas encore de données",
                xaxis_title="Date",
                yaxis_title="Messages"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # ============================================
    # CONVERSATIONS RÉCENTES
    # ============================================
    
    st.subheader("📁 Conversations récentes")
    
    if not conversations:
        st.info("Vous n'avez pas encore de conversations")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📤 Importer votre premier CSV", key="dashboard_first_import", use_container_width=True):
                st.session_state.page = "import_csv"
                st.rerun()
    else:
        # Données pour le tableau
        files_data = {
            "Nom": [],
            "Messages": [],
            "Dernier message": [],
            "Créée le": [],
        }
        
        for conv in conversations[:5]:
            messages = get_messages_by_conversation(conv['id'])
            msg_count = len(messages)
            
            last_msg_date = "Jamais"
            if messages:
                last_msg_date = messages[-1].get('created_at', '')[:16].replace('T', ' ')
            
            created_date = conv.get('created_at', '')[:10] if conv.get('created_at') else ''
            
            files_data["Nom"].append(conv.get('name', 'Sans nom'))
            files_data["Messages"].append(msg_count)
            files_data["Dernier message"].append(last_msg_date)
            files_data["Créée le"].append(created_date)
        
        df_files = pd.DataFrame(files_data)
        st.dataframe(
            df_files,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Nom": st.column_config.TextColumn("Conversation", width="large"),
                "Messages": st.column_config.NumberColumn("Messages", width="small"),
                "Dernier message": st.column_config.TextColumn("Dernier message", width="medium"),
                "Créée le": st.column_config.DateColumn("Créée le", width="medium"),
            }
        )
        
        # Boutons d'action
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("📁 Voir toutes", key="dashboard_view_all", use_container_width=True):
                st.session_state.page = "csv_list"
                st.rerun()
        with col2:
            if st.button("📤 Importer", key="dashboard_import", use_container_width=True):
                st.session_state.page = "import_csv"
                st.rerun()
    
    st.divider()
    
    # ============================================
    # TOP CONVERSATIONS (basé sur données réelles)
    # ============================================
    
    if conversations:
        st.subheader("🔥 Conversations les plus actives")
        
        # Calculer le nombre de messages par conversation
        conv_stats = []
        for conv in conversations:
            messages = get_messages_by_conversation(conv['id'])
            if messages:  # Ne montrer que les conversations avec des messages
                conv_stats.append({
                    'nom': conv.get('name', 'Sans nom'),
                    'messages': len(messages),
                    'id': conv['id']
                })
        
        if conv_stats:
            # Trier par nombre de messages
            top_convs = sorted(conv_stats, key=lambda x: x['messages'], reverse=True)[:3]
            
            cols = st.columns(3)
            for i, conv in enumerate(top_convs):
                with cols[i]:
                    st.markdown(f"""
                    <div style="background: #f8fafc; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e2e8f0;">
                        <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 10px;">{conv['nom'][:20]}</div>
                        <div style="font-size: 2rem; color: #667eea; margin: 10px 0;">{conv['messages']}</div>
                        <div style="font-size: 0.9rem; color: #666; margin-bottom: 15px;">messages</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Ouvrir", key=f"dashboard_open_top_{i}", use_container_width=True):
                        st.session_state.current_conversation = conv['id']
                        st.session_state.page = "conversation"
                        st.rerun()
        else:
            st.info("Aucune conversation avec des messages pour le moment")