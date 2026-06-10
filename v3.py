import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Mon Road Trip en Italie",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #FEF3C7 0%, #FED7AA 50%, #FECACA 100%);
    }
    .header-custom {
        padding: 3rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        background-size: cover;
        background-position: center;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .header-title {
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .header-subtitle {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .activity-card {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .activity-title {
        font-size: 2.2rem;
        font-weight: bold;
        margin: 0 0 0.5rem 0;
        color: #1F2937;
    }
    .activity-location {
        font-size: 1.1rem;
        color: #DC2626;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    .carousel-container {
        position: relative;
        width: 100%;
        margin-bottom: 1.5rem;
        border-radius: 8px;
        overflow: hidden;
    }
    .carousel-image {
        width: 100%;
        border-radius: 8px;
        cursor: pointer;
    }
    .carousel-controls {
        text-align: center;
        margin-top: 0.8rem;
        font-size: 0.9rem;
        color: #666;
    }
    .image-description {
        background: #F9FAFB;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3B82F6;
    }
    .image-description-label {
        font-weight: bold;
        color: #333;
    }
    .image-description-text {
        color: #333;
        margin-top: 0.5rem;
        white-space: pre-wrap;
    }
    .comment-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border-left: 4px solid #3B82F6;
    }
    .comment-name {
        font-weight: bold;
        color: black;
        display: inline;
    }
    .comment-date {
        color: #666;
        font-size: 0.85rem;
        display: inline;
        margin-left: 1rem;
    }
    .comment-text {
        color: black;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Fichier de données
DATA_FILE = "italy_activities.json"
SETTINGS_FILE = "italy_settings.json"

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

# Charger les paramètres du header
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "header_image": None,
        "title": "Mon Road Trip en Italie",
        "subtitle": "Découvrez mon incroyable voyage à travers l'Italie",
        "text_color": "#FFFFFF"
    }

# Sauvegarder les paramètres
def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

# Initialiser la session
if 'activities' not in st.session_state:
    st.session_state.activities = load_data()

if 'settings' not in st.session_state:
    st.session_state.settings = load_settings()

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if 'carousel_index' not in st.session_state:
    st.session_state.carousel_index = {}

# Barre latérale - Authentification Admin
with st.sidebar:
    st.header("🔐 Admin")
    
    if not st.session_state.is_admin:
        password = st.text_input("Mot de passe admin:", type="password", key="admin_password_input")
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

# MODE ADMIN - Personnaliser le header
if st.session_state.is_admin:
    st.markdown("---")
    st.header("🎨 Personnaliser le header")
    
    with st.form("header_form", clear_on_submit=False):
        st.subheader("Texte du header")
        new_title = st.text_input("Titre:", value=st.session_state.settings.get("title", "Mon Road Trip en Italie"))
        new_subtitle = st.text_area("Sous-titre:", value=st.session_state.settings.get("subtitle", "Découvrez mon incroyable voyage à travers l'Italie"), height=80)
        
        st.subheader("Style")
        new_text_color = st.color_picker("Couleur du texte:", value=st.session_state.settings.get("text_color", "#FFFFFF"))
        
        st.subheader("Image de fond")
        st.info("Uploader une image pour le fond du header (JPG, PNG, etc.)")
        header_image = st.file_uploader("Image de fond du header", type=["jpg", "jpeg", "png", "webp"], key="header_image_upload")
        
        header_image_base64 = None
        if header_image:
            bytes_data = header_image.read()
            header_image_base64 = base64.b64encode(bytes_data).decode()
            mime_type = header_image.type
            header_image_base64 = f"data:{mime_type};base64,{header_image_base64}"
        
        if st.form_submit_button("✓ Sauvegarder le header"):
            st.session_state.settings["title"] = new_title
            st.session_state.settings["subtitle"] = new_subtitle
            st.session_state.settings["text_color"] = new_text_color
            if header_image_base64:
                st.session_state.settings["header_image"] = header_image_base64
            save_settings(st.session_state.settings)
            st.success("✓ Header mis à jour!")
            st.rerun()

# Afficher le header personnalisé
settings = st.session_state.settings
header_bg = f"background-image: url('{settings.get('header_image')}'); background-size: cover; background-position: center;" if settings.get("header_image") else f"background: linear-gradient(90deg, #DC2626 0%, #F59E0B 100%);"

header_html = f"""
<div style='{header_bg} padding: 3rem; border-radius: 10px; text-align: center; margin-bottom: 2rem; min-height: 250px; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
    <h1 style='font-size: 3rem; font-weight: bold; color: {settings.get("text_color", "#FFFFFF")}; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{settings.get("title", "Mon Road Trip en Italie")}</h1>
    <p style='font-size: 1.2rem; color: {settings.get("text_color", "#FFFFFF")}; margin-top: 0.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>{settings.get("subtitle", "Découvrez mon incroyable voyage")}</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# MODE ADMIN - Ajouter une nouvelle activité
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
        
        description = st.text_area("📝 Description de l'activité", height=120)
        
        st.subheader("📸 Ajouter des photos")
        st.info("✅ Uploader depuis votre galerie/ordinateur (JPG, PNG, etc.)")
        
        uploaded_files = st.file_uploader(
            "Choisissez vos photos",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            accept_multiple_files=True,
            key="activity_photos"
        )
        
        photo_urls = []
        if uploaded_files:
            preview_cols = st.columns(min(3, len(uploaded_files)))
            for idx, uploaded_file in enumerate(uploaded_files):
                with preview_cols[idx % len(preview_cols)]:
                    st.image(uploaded_file, use_column_width=True)
            
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                base64_image = base64.b64encode(bytes_data).decode()
                mime_type = uploaded_file.type
                photo_urls.append(f"data:{mime_type};base64,{base64_image}")
        
        st.write("**Ou** collez une URL d'image Internet (optionnel):")
        photo_url_input = st.text_input("URL d'image (https://...)", key="photo_url_manual")
        if photo_url_input:
            photo_urls.append(photo_url_input)
        
        # Description pour les images
        image_description = st.text_area("📝 Description des images (visible par les visiteurs)", height=100, key="image_description_input")
        
        if st.form_submit_button("✓ Publier cette activité", use_container_width=True):
            if title and location and photo_urls:
                new_activity = {
                    "id": datetime.now().timestamp(),
                    "title": title,
                    "location": location,
                    "date": str(date),
                    "description": description,
                    "photos": photo_urls,
                    "image_description": image_description,
                    "likes": 0,
                    "comments": []
                }
                st.session_state.activities.append(new_activity)
                save_data(st.session_state.activities)
                st.success("✓ Activité publiée!")
                st.rerun()
            else:
                st.error("Veuillez remplir le titre, la localisation et ajouter au moins une photo")

# Affichage des activités
st.markdown("---")
st.header("📍 Les actus du jour")

if not st.session_state.activities:
    st.info("Aucune activité publiée encore... Commencez par ajouter votre première aventure!")
else:
    for idx, activity in enumerate(st.session_state.activities):
        with st.container():
            st.markdown(f"<div class='activity-card'>", unsafe_allow_html=True)
            
            # Titre et localisation en haut
            st.markdown(f"<div class='activity-title'>{activity['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='activity-location'>📍 {activity.get('location', '')}</div>", unsafe_allow_html=True)
            
            if activity.get("date"):
                st.write(f"📅 {activity['date']}")
            
            # Carousel d'images
            if activity.get("photos"):
                carousel_key = f"carousel_{idx}"
                if carousel_key not in st.session_state.carousel_index:
                    st.session_state.carousel_index[carousel_key] = 0
                
                current_idx = st.session_state.carousel_index[carousel_key]
                photo = activity["photos"][current_idx]
                
                # Afficher l'image (cliquable pour agrandir)
                st.markdown(f"<div class='carousel-container'>", unsafe_allow_html=True)
                try:
                    st.image(photo, use_column_width=True, caption="Cliquez pour agrandir")
                except:
                    st.warning("Impossible de charger la photo")
                st.markdown(f"</div>", unsafe_allow_html=True)
                
                # Contrôles du carousel
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("⬅️ Précédent", key=f"prev_{idx}"):
                        st.session_state.carousel_index[carousel_key] = (current_idx - 1) % len(activity["photos"])
                        st.rerun()
                
                with col2:
                    st.markdown(f"<p style='text-align: center; color: #666;'>Photo {current_idx + 1} sur {len(activity['photos'])}</p>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("Suivant ➡️", key=f"next_{idx}"):
                        st.session_state.carousel_index[carousel_key] = (current_idx + 1) % len(activity["photos"])
                        st.rerun()
            
            # Description des images
            if activity.get("image_description"):
                st.markdown(f"""
                <div class='image-description'>
                    <span class='image-description-label'>Description :</span>
                    <div class='image-description-text'>{activity['image_description']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Description générale
            if activity.get("description"):
                st.write(activity["description"])
            
            st.markdown("---")
            
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
                    st.markdown(f"""
                    <div class='comment-box'>
                        <span class='comment-name'>{comment['name']}</span>
                        <span class='comment-date'>{comment['date']}</span>
                        <div class='comment-text'>{comment['text']}</div>
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
            
            st.markdown(f"</div>", unsafe_allow_html=True)
            st.markdown("---")
