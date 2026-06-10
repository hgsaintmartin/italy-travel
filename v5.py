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

# Styles CSS - MODE LUMIÈRE
st.markdown("""
    <style>
    :root {
        --primary-color: #DC2626;
        --secondary-color: #F59E0B;
        --light-bg: #FFFFFF;
        --text-dark: #1F2937;
        --text-gray: #6B7280;
        --border-color: #E5E7EB;
    }
    
    body, .main {
        background-color: #F9FAFB !important;
    }
    
    .header-custom {
        padding: 3rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    
    .header-custom::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.35);
        z-index: 1;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        color: #FFFFFF;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        color: #FFFFFF;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    
    .activity-card {
        background: white;
        border-radius: 12px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #E5E7EB;
    }
    
    .activity-title {
        font-size: 2.2rem;
        font-weight: 800;
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
        border-radius: 10px;
        overflow: hidden;
        background: #F3F4F6;
    }
    
    .carousel-image {
        width: 100%;
        border-radius: 10px;
        display: block;
    }
    
    .carousel-thumbnails {
        display: flex;
        gap: 0.8rem;
        margin-top: 1.2rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .carousel-thumb-btn {
        border: 3px solid transparent;
        border-radius: 8px;
        overflow: hidden;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 90px;
        height: 90px;
        padding: 0 !important;
        background: none !important;
    }
    
    .carousel-thumb-btn:hover {
        border-color: #F59E0B;
        transform: scale(1.05);
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .carousel-thumb-btn.active {
        border-color: #DC2626;
        transform: scale(1.08);
        box-shadow: 0 4px 10px rgba(220, 38, 38, 0.3);
    }
    
    .carousel-thumb-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .carousel-controls {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .carousel-counter {
        text-align: center;
        color: #6B7280;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .image-description {
        background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3B82F6;
    }
    
    .image-description-label {
        font-weight: 700;
        color: #1F2937;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .image-description-text {
        color: #374151;
        margin-top: 0.5rem;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    
    .comment-box {
        background: white;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border-left: 4px solid #3B82F6;
        border: 1px solid #E5E7EB;
    }
    
    .comment-name {
        font-weight: 700;
        color: #1F2937;
        display: inline;
    }
    
    .comment-date {
        color: #9CA3AF;
        font-size: 0.85rem;
        display: inline;
        margin-left: 1rem;
    }
    
    .comment-text {
        color: #374151;
        margin-top: 0.5rem;
        line-height: 1.6;
    }
    
    [data-testid="stButton"] button {
        color: white !important;
        font-weight: 600;
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

if 'editing_activity' not in st.session_state:
    st.session_state.editing_activity = None

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
header_bg_style = ""
if settings.get("header_image"):
    header_bg_style = f"background-image: url('{settings.get('header_image')}');"
else:
    header_bg_style = "background: linear-gradient(135deg, #DC2626 0%, #F59E0B 100%);"

header_html = f"""
<div style='{header_bg_style} background-size: cover; background-position: center; padding: 3rem; border-radius: 10px; text-align: center; margin-bottom: 2rem; min-height: 280px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; overflow: hidden;'>
    <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.35); z-index: 1;'></div>
    <div style='position: relative; z-index: 2;'>
        <h1 style='font-size: 3rem; font-weight: 900; color: {settings.get("text_color", "#FFFFFF")}; margin: 0; text-shadow: 2px 2px 6px rgba(0,0,0,0.5);'>{settings.get("title", "Mon Road Trip en Italie")}</h1>
        <p style='font-size: 1.2rem; color: {settings.get("text_color", "#FFFFFF")}; margin-top: 0.5rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);'>{settings.get("subtitle", "Découvrez mon incroyable voyage")}</p>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# MODE ADMIN - Ajouter une nouvelle activité
if st.session_state.is_admin:
    st.markdown("---")
    
    if st.session_state.editing_activity is not None:
        st.header("✏️ Modifier l'activité")
        editing_idx = st.session_state.editing_activity
        activity = st.session_state.activities[editing_idx]
    else:
        st.header("➕ Ajouter une nouvelle activité")
        activity = None
    
    with st.form("activity_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📌 Titre de l'activité", value=activity["title"] if activity else "")
            location = st.text_input("📍 Localisation", value=activity["location"] if activity else "")
        
        with col2:
            date = st.date_input("📅 Date", value=datetime.strptime(activity["date"], "%Y-%m-%d").date() if activity and activity.get("date") else datetime.now().date())
        
        description = st.text_area("📝 Description de l'activité", height=120, value=activity["description"] if activity else "")
        
        st.subheader("📸 Ajouter des photos")
        st.info("✅ Uploader depuis votre galerie/ordinateur (JPG, PNG, etc.)")
        
        uploaded_files = st.file_uploader(
            "Choisissez vos photos",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            accept_multiple_files=True,
            key="activity_photos"
        )
        
        photo_urls = []
        if activity and activity.get("photos"):
            st.write("**Photos actuelles:**")
            for photo_idx, photo in enumerate(activity.get("photos", [])):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"Photo {photo_idx + 1}")
                with col2:
                    if st.button("🗑️", key=f"delete_photo_{photo_idx}"):
                        activity["photos"].pop(photo_idx)
                        save_data(st.session_state.activities)
                        st.rerun()
        
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
        image_description = st.text_area("📝 Description des images (visible par les visiteurs)", height=100, value=activity["image_description"] if activity and activity.get("image_description") else "", key="image_description_input")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("✓ " + ("Mettre à jour" if activity else "Publier"), use_container_width=True)
        with col2:
            if activity:
                cancel_button = st.form_submit_button("❌ Annuler", use_container_width=True)
            else:
                cancel_button = False
        
        if submit_button:
            if title and location:
                if activity:
                    # Mettre à jour l'activité existante
                    st.session_state.activities[editing_idx]["title"] = title
                    st.session_state.activities[editing_idx]["location"] = location
                    st.session_state.activities[editing_idx]["date"] = str(date)
                    st.session_state.activities[editing_idx]["description"] = description
                    st.session_state.activities[editing_idx]["image_description"] = image_description
                    if photo_urls:
                        st.session_state.activities[editing_idx]["photos"].extend(photo_urls)
                    save_data(st.session_state.activities)
                    st.session_state.editing_activity = None
                    st.success("✓ Activité mise à jour!")
                else:
                    # Créer une nouvelle activité
                    if photo_urls:
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
                    else:
                        st.error("Veuillez ajouter au moins une photo")
                st.rerun()
            else:
                st.error("Veuillez remplir le titre et la localisation")
        
        if cancel_button and activity:
            st.session_state.editing_activity = None
            st.rerun()

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
                
                # Afficher l'image principale
                st.markdown(f"<div class='carousel-container'>", unsafe_allow_html=True)
                try:
                    st.image(photo, use_column_width=True)
                except:
                    st.warning("Impossible de charger la photo")
                st.markdown(f"</div>", unsafe_allow_html=True)
                
                # Boutons défiler
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("⬅️ Précédent", key=f"prev_{idx}"):
                        st.session_state.carousel_index[carousel_key] = (current_idx - 1) % len(activity["photos"])
                        st.rerun()
                
                with col2:
                    st.markdown(f"<p class='carousel-counter'>Photo {current_idx + 1} sur {len(activity['photos'])}</p>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("Suivant ➡️", key=f"next_{idx}"):
                        st.session_state.carousel_index[carousel_key] = (current_idx + 1) % len(activity["photos"])
                        st.rerun()
                
                # Miniatures cliquables en dessous
                if len(activity["photos"]) > 1:
                    st.markdown("<div class='carousel-thumbnails'>", unsafe_allow_html=True)
                    thumb_cols = st.columns(min(6, len(activity["photos"])))
                    for thumb_idx, thumb_photo in enumerate(activity["photos"]):
                        with thumb_cols[thumb_idx % len(thumb_cols)]:
                            if st.button(
                                "",
                                key=f"thumb_{idx}_{thumb_idx}",
                                use_container_width=True,
                                help=f"Photo {thumb_idx + 1}"
                            ):
                                st.session_state.carousel_index[carousel_key] = thumb_idx
                                st.rerun()
                            # Afficher la miniature
                            st.markdown(f"""
                            <img src="{thumb_photo}" class="carousel-thumb-img" style="width: 100%; height: 100%; border-radius: 8px; border: 3px solid {'#DC2626' if thumb_idx == current_idx else '#E5E7EB'}; object-fit: cover; cursor: pointer;">
                            """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
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
                        st.session_state.editing_activity = idx
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Supprimer", key=f"delete_{idx}"):
                        st.session_state.activities.pop(idx)
                        save_data(st.session_state.activities)
                        st.success("Activité supprimée!")
                        st.rerun()
            
            st.markdown(f"</div>", unsafe_allow_html=True)
            st.markdown("---")
