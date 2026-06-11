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
    
    .header-title {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        color: #FFFFFF;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
        position: relative;
        z-index: 2;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        color: #FFFFFF;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        position: relative;
        z-index: 2;
    }
    
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem;
        margin: 1.5rem 0;
    }
    
    @media (max-width: 768px) {
        .grid-container {
            grid-template-columns: repeat(4, 1fr);
            gap: 0.6rem;
        }
    }
    
    .grid-item {
        cursor: pointer;
    }
    
    .grid-item img {
        width: 100%;
        aspect-ratio: 1;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        transition: transform 0.3s ease;
    }
    
    .grid-item img:hover {
        transform: scale(1.05);
    }
    
    .grid-title {
        padding: 0.6rem;
        background: white;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #E5E7EB;
    }
    
    .grid-title p {
        margin: 0;
    }
    
    .grid-title-text {
        font-weight: 600;
        color: #1F2937;
        font-size: 0.75rem;
    }
    
    .grid-date {
        font-size: 0.65rem;
        color: #6B7280;
        margin-top: 0.2rem;
    }
    
    .activity-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #E5E7EB;
    }
    
    .activity-title {
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: #1F2937;
    }
    
    .activity-location {
        font-size: 1rem;
        color: #DC2626;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    
    .image-description {
        background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        border-left: 4px solid #3B82F6;
    }
    
    .image-description-label {
        font-weight: 700;
        color: #1F2937;
    }
    
    .image-description-text {
        color: #374151;
        margin-top: 0.5rem;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    
    .comment-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border: 1px solid #E5E7EB;
    }
    
    .comment-name {
        font-weight: 700;
        color: #1F2937;
    }
    
    .comment-date {
        color: #9CA3AF;
        font-size: 0.85rem;
        margin-left: 1rem;
    }
    
    .comment-text {
        color: #374151;
        margin-top: 0.5rem;
    }
    
    .program-box {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        font-size: 0.9rem;
        line-height: 1.8;
        color: #374151;
    }
    
    </style>
""", unsafe_allow_html=True)

# Fichier de données
DATA_FILE = "italy_activities.json"
SETTINGS_FILE = "italy_settings.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "header_image": None,
        "title": "Mon Road Trip en Italie",
        "subtitle": "Découvrez mon incroyable voyage à travers l'Italie",
        "text_color": "#FFFFFF",
        "actu_text": "Bienvenue sur mon blog de voyage!"
    }

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

if 'selected_post' not in st.session_state:
    st.session_state.selected_post = None

# Sidebar
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
    
    st.markdown("---")
    st.subheader("📋 Programme")
    
    program_text = """
**Programme**

21-23 Rome
23-27 Rome with AB
27-02 Florence
02-04 Venise
04-05 Palerme
06 Cefalù
07 Agrigente
08-10 Palerme
10 🛩️
"""
    st.markdown(f"<div class='program-box'>{program_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

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
        <h1 style='font-size: 3rem; font-weight: 900; color: {settings.get("text_color", "#FFFFFF")}; margin: 0;'>{settings.get("title", "Mon Road Trip en Italie")}</h1>
        <p style='font-size: 1.2rem; color: {settings.get("text_color", "#FFFFFF")}; margin-top: 0.5rem;'>{settings.get("subtitle", "Découvrez mon incroyable voyage")}</p>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# MODE ADMIN - Personnaliser le header
if st.session_state.is_admin:
    with st.expander("🎨 Personnaliser le header"):
        with st.form("header_form", clear_on_submit=False):
            new_title = st.text_input("Titre:", value=settings.get("title", ""))
            new_subtitle = st.text_area("Sous-titre:", value=settings.get("subtitle", ""), height=60)
            new_text_color = st.color_picker("Couleur du texte:", value=settings.get("text_color", "#FFFFFF"))
            
            header_image = st.file_uploader("Image de fond:", type=["jpg", "jpeg", "png", "webp"], key="header_image_upload_unique")
            
            header_image_base64 = None
            if header_image:
                bytes_data = header_image.read()
                header_image_base64 = base64.b64encode(bytes_data).decode()
                mime_type = header_image.type
                header_image_base64 = f"data:{mime_type};base64,{header_image_base64}"
            
            if st.form_submit_button("✓ Sauvegarder"):
                st.session_state.settings["title"] = new_title
                st.session_state.settings["subtitle"] = new_subtitle
                st.session_state.settings["text_color"] = new_text_color
                if header_image_base64:
                    st.session_state.settings["header_image"] = header_image_base64
                save_settings(st.session_state.settings)
                st.success("✓ Mis à jour!")
                st.rerun()

# Section "Les actus du jour"
st.header("📍 Les actus du jour")

if st.session_state.is_admin:
    with st.expander("✏️ Modifier le texte"):
        new_actu_text = st.text_area("Texte des actualités:", value=settings.get("actu_text", ""), height=100, key="actu_text_unique")
        if st.button("✓ Sauvegarder"):
            st.session_state.settings["actu_text"] = new_actu_text
            save_settings(st.session_state.settings)
            st.success("✓ Mis à jour!")

st.markdown(settings.get("actu_text", "Bienvenue sur mon blog de voyage!"))

# MODE ADMIN - Ajouter une publication
if st.session_state.is_admin:
    st.markdown("---")
    
    if st.session_state.editing_activity is not None:
        st.header("✏️ Modifier")
        editing_idx = st.session_state.editing_activity
        activity = st.session_state.activities[editing_idx]
    else:
        st.header("➕ Ajouter une nouvelle publication")
        activity = None
    
    with st.form("activity_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📌 Titre", value=activity["title"] if activity else "")
            location = st.text_input("📍 Localisation", value=activity["location"] if activity else "")
        
        with col2:
            date = st.date_input("📅 Date", value=datetime.strptime(activity["date"], "%Y-%m-%d").date() if activity and activity.get("date") else datetime.now().date())
        
        description = st.text_area("📝 Description", height=100, value=activity["description"] if activity else "")
        
        st.subheader("📸 Photos")
        st.info("La première photo sera la couverture")
        
        uploaded_files = st.file_uploader(
            "Photos",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            accept_multiple_files=True,
            key="photos_uploader"
        )
        
        photo_urls = []
        if activity and activity.get("photos"):
            st.write("**Photos actuelles:**")
            for photo_idx in range(len(activity.get("photos", []))):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"Photo {photo_idx + 1}")
                with col2:
                    if st.button("🗑️", key=f"del_photo_{photo_idx}"):
                        activity["photos"].pop(photo_idx)
                        save_data(st.session_state.activities)
                        st.rerun()
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                base64_image = base64.b64encode(bytes_data).decode()
                mime_type = uploaded_file.type
                photo_urls.append(f"data:{mime_type};base64,{base64_image}")
            st.success(f"{len(uploaded_files)} photo(s) à ajouter")
        
        photo_url_input = st.text_input("Ou URL d'image:")
        if photo_url_input:
            photo_urls.append(photo_url_input)
        
        image_description = st.text_area("Description images", height=80, value=activity["image_description"] if activity and activity.get("image_description") else "")
        
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
                    st.session_state.activities[editing_idx]["title"] = title
                    st.session_state.activities[editing_idx]["location"] = location
                    st.session_state.activities[editing_idx]["date"] = str(date)
                    st.session_state.activities[editing_idx]["description"] = description
                    st.session_state.activities[editing_idx]["image_description"] = image_description
                    if photo_urls:
                        st.session_state.activities[editing_idx]["photos"].extend(photo_urls)
                    save_data(st.session_state.activities)
                    st.session_state.editing_activity = None
                    st.success("✓ Mise à jour!")
                else:
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
                        st.success("✓ Publiée!")
                    else:
                        st.error("Ajouter au moins une photo")
                st.rerun()
            else:
                st.error("Remplir titre et localisation")
        
        if cancel_button and activity:
            st.session_state.editing_activity = None
            st.rerun()

# Trier par date (plus récent en premier)
sorted_activities = sorted(st.session_state.activities, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)

# Grille de publications
if not sorted_activities:
    st.info("Aucune publication...")
else:
    st.markdown("---")
    st.subheader("📸 Publications")
    
    # HTML pour la grille
    grid_html = "<div class='grid-container'>"
    
    for idx, activity in enumerate(sorted_activities):
        if activity.get("photos"):
            grid_html += f"""
            <div class='grid-item' onclick="document.getElementById('post_{idx}').click()">
                <img src='{activity['photos'][0]}' alt='{activity['title']}'>
                <div class='grid-title'>
                    <p class='grid-title-text'>{activity['title']}</p>
                    <p class='grid-date'>{activity['date']}</p>
                </div>
            </div>
            """
    
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # Boutons invisibles
    cols = st.columns(4)
    for idx, activity in enumerate(sorted_activities):
        col = cols[idx % 4]
        with col:
            if st.button("Voir", key=f"post_{idx}", use_container_width=False):
                st.session_state.selected_post = idx
                st.rerun()

# Modal
if st.session_state.selected_post is not None:
    activity = sorted_activities[st.session_state.selected_post]
    
    st.markdown("<div style='position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 1000; overflow-y: auto; padding: 2rem;'>", unsafe_allow_html=True)
    st.markdown("<div style='background: white; border-radius: 12px; padding: 2rem; max-width: 900px; margin: auto;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([20, 1])
    with col2:
        if st.button("✕"):
            st.session_state.selected_post = None
            st.rerun()
    
    st.markdown(f"<h2>{activity['title']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #DC2626; font-weight: 600;'>📍 {activity['location']}</p>", unsafe_allow_html=True)
    st.write(f"📅 {activity['date']}")
    
    # Images avec défil
    if activity.get("photos"):
        carousel_key = f"carousel_{st.session_state.selected_post}"
        if carousel_key not in st.session_state.carousel_index:
            st.session_state.carousel_index[carousel_key] = 0
        
        current_idx = st.session_state.carousel_index[carousel_key]
        st.image(activity["photos"][current_idx], use_column_width=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️"):
                st.session_state.carousel_index[carousel_key] = (current_idx - 1) % len(activity["photos"])
                st.rerun()
        with col2:
            st.write(f"📷 {current_idx + 1} / {len(activity['photos'])}")
        with col3:
            if st.button("➡️"):
                st.session_state.carousel_index[carousel_key] = (current_idx + 1) % len(activity["photos"])
                st.rerun()
        
        # Miniatures
        if len(activity["photos"]) > 1:
            st.write("")
            st.markdown("<div style='display: flex; gap: 0.8rem; overflow-x: auto; padding: 1rem; background: #F3F4F6; border-radius: 8px;'>", unsafe_allow_html=True)
            for thumb_idx, thumb_photo in enumerate(activity["photos"]):
                if st.button("", key=f"thumb_{st.session_state.selected_post}_{thumb_idx}"):
                    st.session_state.carousel_index[carousel_key] = thumb_idx
                    st.rerun()
                st.markdown(f"<img src='{thumb_photo}' style='flex: 0 0 100px; height: 100px; border-radius: 6px; border: 3px solid {"#DC2626" if thumb_idx == current_idx else "#E5E7EB"}; object-fit: cover;'>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    if activity.get("image_description"):
        st.markdown(f"""
        <div class='image-description'>
            <p class='image-description-label'>Description :</p>
            <p class='image-description-text'>{activity['image_description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if activity.get("description"):
        st.write(activity["description"])
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"❤️ ({activity.get('likes', 0)})"):
            sorted_activities[st.session_state.selected_post]["likes"] += 1
            st.session_state.activities = sorted_activities
            save_data(st.session_state.activities)
            st.rerun()
    with col2:
        st.write(f"💬 {len(activity.get('comments', []))}")
    
    st.subheader("Commentaire")
    name = st.text_input("Nom:")
    text = st.text_input("Message:")
    if st.button("Publier"):
        if name and text:
            sorted_activities[st.session_state.selected_post]["comments"].append({
                "name": name,
                "text": text,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.session_state.activities = sorted_activities
            save_data(st.session_state.activities)
            st.rerun()
    
    if activity.get("comments"):
        st.subheader("Commentaires")
        for comment in activity["comments"]:
            st.markdown(f"""
            <div class='comment-box'>
                <span class='comment-name'>{comment['name']}</span>
                <span class='comment-date'>{comment['date']}</span>
                <p class='comment-text'>{comment['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if st.session_state.is_admin:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Modifier"):
                st.session_state.editing_activity = st.session_state.activities.index(activity)
                st.session_state.selected_post = None
                st.rerun()
        with col2:
            if st.button("🗑️ Supprimer"):
                st.session_state.activities.remove(activity)
                save_data(st.session_state.activities)
                st.session_state.selected_post = None
                st.success("✓ Supprimée!")
                st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
