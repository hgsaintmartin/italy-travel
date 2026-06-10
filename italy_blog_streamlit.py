import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="🇮🇹 Mon Road Trip en Italie",
    page_icon="🇮🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #FEF3C7 0%, #FED7AA 50%, #FECACA 100%);
    }
    .header {
        background: linear-gradient(90deg, #DC2626 0%, #F59E0B 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .activity-card {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .comment-box {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

# Fichier de données
DATA_FILE = "italy_activities.json"

# Charger les données
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Sauvegarder les données
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Initialiser la session
if 'activities' not in st.session_state:
    st.session_state.activities = load_data()

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Header
st.markdown("""
    <div style='background: linear-gradient(90deg, #DC2626 0%, #F59E0B 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;'>
        <h1>🇮🇹 Mon Road Trip en Italie</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Découvrez mon incroyable voyage à travers l'Italie</p>
    </div>
""", unsafe_allow_html=True)

# Barre latérale - Authentification Admin
with st.sidebar:
    st.header("🔐 Admin")
    
    if not st.session_state.is_admin:
        password = st.text_input("Mot de passe admin:", type="password")
        if st.button("Se connecter"):
            if password == "italy2024":
                st.session_state.is_admin = True
                st.success("Connecté en tant qu'admin !")
                st.rerun()
            else:
                st.error("Mot de passe incorrect")
    else:
        st.success("✓ Mode Admin activé")
        if st.button("Se déconnecter"):
            st.session_state.is_admin = False
            st.rerun()

# MODE ADMIN - Ajouter/Modifier une activité
if st.session_state.is_admin:
    st.markdown("---")
    st.header("➕ Ajouter une nouvelle activité")
    
    with st.form("activity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📌 Titre de l'activité")
            location = st.text_input("📍 Localisation")
        
        with col2:
            date = st.date_input("📅 Date")
        
        description = st.text_area("📝 Description (pas de limite!)", height=150)
        
        st.subheader("📸 Ajouter des photos")
        st.info("Collez l'URL d'une image Internet (URL complète commençant par https://)")
        
        photo_urls = []
        for i in range(1, 6):
            photo_url = st.text_input(f"Photo {i}:", key=f"photo_{i}")
            if photo_url:
                photo_urls.append(photo_url)
        
        if st.form_submit_button("✓ Publier cette activité", use_container_width=True):
            if title and location:
                new_activity = {
                    "id": datetime.now().timestamp(),
                    "title": title,
                    "location": location,
                    "date": str(date),
                    "description": description,
                    "photos": photo_urls,
                    "likes": 0,
                    "comments": []
                }
                st.session_state.activities.append(new_activity)
                save_data(st.session_state.activities)
                st.success("✓ Activité publiée!")
                st.rerun()
            else:
                st.error("Veuillez remplir au moins le titre et la localisation")

# Affichage des activités
st.markdown("---")
st.header("🌍 Vos activités")

if not st.session_state.activities:
    st.info("Aucune activité publiée encore... Commencez par ajouter votre première aventure!")
else:
    for idx, activity in enumerate(st.session_state.activities):
        with st.container():
            # Afficher les photos en galerie
            if activity.get("photos"):
                cols = st.columns(min(3, len(activity["photos"])))
                for col_idx, photo in enumerate(activity["photos"]):
                    with cols[col_idx % len(cols)]:
                        try:
                            st.image(photo, use_column_width=True)
                        except:
                            st.warning(f"Impossible de charger la photo {col_idx + 1}")
            
            # Contenu de l'activité
            st.subheader(activity["title"])
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if activity.get("location"):
                    st.write(f"📍 **{activity['location']}**")
                if activity.get("date"):
                    st.write(f"📅 {activity['date']}")
            
            # Description
            st.write(activity.get("description", ""))
            
            # Interactions (Likes et Commentaires)
            col_like, col_comment = st.columns(2)
            
            with col_like:
                if st.button(f"❤️ J'aime ({activity.get('likes', 0)})", key=f"like_{idx}"):
                    st.session_state.activities[idx]["likes"] = activity.get("likes", 0) + 1
                    save_data(st.session_state.activities)
                    st.rerun()
            
            with col_comment:
                st.write(f"💬 {len(activity.get('comments', []))} commentaire(s)")
            
            # Formulaire commentaire
            st.subheader("Ajouter un commentaire")
            col1, col2 = st.columns(2)
            with col1:
                commenter_name = st.text_input("Votre nom:", key=f"name_{idx}")
            with col2:
                commenter_text = st.text_input("Votre commentaire:", key=f"comment_{idx}")
            
            if st.button("Publier le commentaire", key=f"submit_comment_{idx}"):
                if commenter_name and commenter_text:
                    new_comment = {
                        "name": commenter_name,
                        "text": commenter_text,
                        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    st.session_state.activities[idx]["comments"].append(new_comment)
                    save_data(st.session_state.activities)
                    st.success("Commentaire publié!")
                    st.rerun()
                else:
                    st.error("Veuillez remplir votre nom et votre commentaire")
            
            # Afficher les commentaires
            if activity.get("comments"):
                st.subheader("Commentaires")
                for comment in activity["comments"]:
                    with st.container():
                        st.markdown(f"""
                        <div style='background: #F3F4F6; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #3B82F6;'>
                            <p><b>{comment['name']}</b> <i style='color: #999;'>{comment['date']}</i></p>
                            <p>{comment['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Boutons Admin
            if st.session_state.is_admin:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Modifier", key=f"edit_{idx}"):
                        st.info("Fonction de modification: Supprimez cette activité et créez-la à nouveau")
                
                with col2:
                    if st.button("🗑️ Supprimer", key=f"delete_{idx}"):
                        st.session_state.activities.pop(idx)
                        save_data(st.session_state.activities)
                        st.success("Activité supprimée!")
                        st.rerun()
            
            st.markdown("---")

# Footer
st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 3rem; padding: 2rem;'>
        <p>🇮🇹 <b>Buon viaggio!</b> Partage ce lien avec tes amis pour suivre mon aventure 🌍</p>
    </div>
""", unsafe_allow_html=True)
