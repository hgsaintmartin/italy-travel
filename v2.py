import streamlit as st
import json
import os
from datetime import datetime
import base64
import io
from zipfile import ZipFile
import requests

st.set_page_config(page_title="Mon Road Trip en Italie", page_icon="✈️", layout="wide")

st.markdown("""
<style>
body { background-color: #F9FAFB !important; }
.header { padding: 3rem; border-radius: 10px; text-align: center; margin-bottom: 2rem; background-size: cover; background-position: center; min-height: 250px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }
.header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.35); border-radius: 10px; }
.header h1, .header p { position: relative; z-index: 2; color: white; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); margin: 0; }
.post-card { background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #E5E7EB; text-align: center; }
.post-card p { margin: 0.5rem 0 0 0; }
.program-box { background: white; border-radius: 10px; padding: 1.5rem; text-align: center; font-size: 0.9rem; line-height: 1.8; color: #374151; }
.publication-box { background: white; border: 2px solid #E5E7EB; border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.pub-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 2px solid #E5E7EB; }
.pub-title { font-size: 1.5rem; font-weight: 800; color: #1F2937; margin: 0; }
.pub-date { font-size: 0.85rem; color: #6B7280; margin-top: 0.3rem; }
.pub-location { font-size: 1rem; color: #DC2626; font-weight: 600; }
.pub-description { background: #F9FAFB; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #3B82F6; color: #374151; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "italy_activities.json"
SETTINGS_FILE = "italy_settings.json"

def load_data():
    return json.load(open(DATA_FILE)) if os.path.exists(DATA_FILE) else []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        return json.load(open(SETTINGS_FILE))
    return {"header_image": None, "title": "Mon Road Trip en Italie", "subtitle": "Découvrez mon incroyable voyage", "text_color": "#FFFFFF", "actu_text": "Bienvenue!"}

def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)

def create_zip_download(photos, title):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for idx, photo in enumerate(photos):
            try:
                if photo.startswith('data:'):
                    header, data = photo.split(',', 1)
                    image_data = base64.b64decode(data)
                    ext = 'jpg'
                    if 'png' in header:
                        ext = 'png'
                    elif 'gif' in header:
                        ext = 'gif'
                    zip_file.writestr(f"photo_{idx+1}.{ext}", image_data)
                else:
                    try:
                        response = requests.get(photo, timeout=5)
                        if response.status_code == 200:
                            ext = 'jpg'
                            if 'png' in response.headers.get('content-type', ''):
                                ext = 'png'
                            zip_file.writestr(f"photo_{idx+1}.{ext}", response.content)
                    except:
                        pass
            except:
                pass
    zip_buffer.seek(0)
    return zip_buffer

if 'activities' not in st.session_state:
    st.session_state.activities = load_data()
if 'settings' not in st.session_state:
    st.session_state.settings = load_settings()
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_post_idx' not in st.session_state:
    st.session_state.selected_post_idx = None
if 'carousel_idx' not in st.session_state:
    st.session_state.carousel_idx = 0
if 'editing_idx' not in st.session_state:
    st.session_state.editing_idx = None

with st.sidebar:
    st.header("🔐 Admin")
    if not st.session_state.is_admin:
        pw = st.text_input("Mot de passe:", type="password", key="pw_input")
        if st.button("Connexion"):
            if pw == "italy2024":
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("❌")
    else:
        st.success("✓ Admin")
        if st.button("Déconnexion"):
            st.session_state.is_admin = False
            st.rerun()
    
    st.markdown("---")
    st.subheader("📋 Programme")
    prog = "**Programme**\n\n21-23 Rome\n23-27 Rome with AB\n27-02 Florence\n02-04 Venise\n04-05 Palerme\n06 Cefalù\n07 Agrigente\n08-10 Palerme\n10 🛩️"
    st.markdown(f"<div class='program-box'>{prog.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

# HEADER
s = st.session_state.settings
bg = f"background-image: url('{s.get('header_image')}');" if s.get('header_image') else "background: linear-gradient(135deg, #DC2626 0%, #F59E0B 100%);"
st.markdown(f"""
<div style='{bg} padding: 3rem; border-radius: 10px; text-align: center; margin-bottom: 2rem; min-height: 250px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative;'>
    <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.35); border-radius: 10px;'></div>
    <div style='position: relative; z-index: 2;'>
        <h1 style='font-size: 3rem; font-weight: 900; color: {s.get("text_color")}; margin: 0;'>{s.get("title")}</h1>
        <p style='font-size: 1.2rem; color: {s.get("text_color")}; margin-top: 0.5rem;'>{s.get("subtitle")}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ADMIN SETTINGS
if st.session_state.is_admin:
    with st.expander("🎨 Personnaliser"):
        with st.form("header_form", clear_on_submit=False):
            title = st.text_input("Titre:", s.get("title"), key="hdr_title")
            subtitle = st.text_area("Sous-titre:", s.get("subtitle"), height=60, key="hdr_subtitle")
            color = st.color_picker("Couleur texte:", s.get("text_color"), key="hdr_color")
            img = st.file_uploader("Image fond:", type=["jpg", "jpeg", "png", "webp"], key="hdr_img")
            
            if st.form_submit_button("✓"):
                img_b64 = None
                if img:
                    img_b64 = f"data:{img.type};base64,{base64.b64encode(img.read()).decode()}"
                s["title"] = title
                s["subtitle"] = subtitle
                s["text_color"] = color
                if img_b64:
                    s["header_image"] = img_b64
                save_settings(s)
                st.success("✓")
                st.rerun()

# ACCUEIL
if st.session_state.view == 'home':
    st.header("📍 Les actus du jour")
    
    if st.session_state.is_admin:
        with st.expander("✏️ Texte"):
            txt = st.text_area("Texte:", s.get("actu_text", ""), height=80, key="actu_text_edit")
            if st.button("Sauvegarder"):
                s["actu_text"] = txt
                save_settings(s)
                st.success("✓")
    
    st.markdown(s.get("actu_text", ""))
    
    # AJOUTER PUBLICATION
    if st.session_state.is_admin:
        st.markdown("---")
        st.header("➕ Nouvelle publication")
        
        if st.session_state.editing_idx is not None:
            a = st.session_state.activities[st.session_state.editing_idx]
            st.info(f"✏️ Modification de: {a['title']}")
        else:
            a = None
        
        with st.form("post_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Titre:", value=a["title"] if a else "", key="post_title")
                loc = st.text_input("Localisation:", value=a["location"] if a else "", key="post_loc")
            with col2:
                d = st.date_input("Date:", value=datetime.strptime(a["date"], "%Y-%m-%d").date() if a else datetime.now(), key="post_date")
            
            desc = st.text_area("Description:", value=a["description"] if a else "", height=80, key="post_desc")
            
            st.subheader("📸 Photos")
            
            # Photos actuelles avec suppression
            if a and a.get("photos"):
                st.write(f"**{len(a['photos'])} photo(s) actuelles :**")
                for i in range(len(a["photos"])):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.text(f"Photo {i + 1}")
                    with col2:
                        if st.button("❌", key=f"del_photo_{i}"):
                            a["photos"].pop(i)
                            save_data(st.session_state.activities)
                            st.rerun()
                st.markdown("---")
            
            files = st.file_uploader("Ajouter photos:", accept_multiple_files=True, type=["jpg", "jpeg", "png", "gif", "webp"], key="post_photos")
            
            photos = []
            if files:
                for f in files:
                    photos.append(f"data:{f.type};base64,{base64.b64encode(f.read()).decode()}")
            
            url = st.text_input("Ou URL:", key="post_url")
            if url:
                photos.append(url)
            
            img_desc = st.text_area("Description images:", value=a["image_description"] if a else "", height=60, key="post_img_desc")
            
            col1, col2 = st.columns(2)
            with col1:
                sub = st.form_submit_button("✓ " + ("Mettre à jour" if a else "Publier"), use_container_width=True)
            with col2:
                if a and st.form_submit_button("❌ Annuler", use_container_width=True):
                    st.session_state.editing_idx = None
                    st.rerun()
            
            if sub:
                if title and loc:
                    final_photos = (a["photos"] if a else []) + photos
                    if final_photos:
                        if a:
                            st.session_state.activities[st.session_state.editing_idx]["title"] = title
                            st.session_state.activities[st.session_state.editing_idx]["location"] = loc
                            st.session_state.activities[st.session_state.editing_idx]["date"] = str(d)
                            st.session_state.activities[st.session_state.editing_idx]["description"] = desc
                            st.session_state.activities[st.session_state.editing_idx]["image_description"] = img_desc
                            st.session_state.activities[st.session_state.editing_idx]["photos"] = final_photos
                            save_data(st.session_state.activities)
                            st.session_state.editing_idx = None
                            st.success("✓ Mise à jour!")
                            st.rerun()
                        else:
                            st.session_state.activities.append({
                                "id": datetime.now().timestamp(),
                                "title": title,
                                "location": loc,
                                "date": str(d),
                                "description": desc,
                                "photos": final_photos,
                                "image_description": img_desc,
                                "likes": 0,
                                "comments": []
                            })
                            save_data(st.session_state.activities)
                            st.success("✓ Publiée!")
                            st.rerun()
                    else:
                        st.error("Ajouter au moins une photo")
                else:
                    st.error("Remplir titre et localisation")
    
    # GRILLE PUBLICATIONS
    st.markdown("---")
    st.subheader("📸 Publications")
    
    sorted_acts = sorted(st.session_state.activities, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    
    if not sorted_acts:
        st.info("Aucune publication")
    else:
        cols = st.columns(4)
        for idx, act in enumerate(sorted_acts):
            col = cols[idx % 4]
            with col:
                if act.get("photos"):
                    st.image(act["photos"][0], use_column_width=True)
                
                if st.button(act["title"], key=f"view_{idx}", use_container_width=True):
                    st.session_state.view = 'post'
                    st.session_state.selected_post_idx = idx
                    st.session_state.carousel_idx = 0
                    st.rerun()
                
                st.markdown(f"<div class='post-card'><p style='color: #DC2626; font-weight: 600;'>{act['location']}</p><p style='color: #6B7280; font-size: 0.85rem;'>{act['date']}</p></div>", unsafe_allow_html=True)

# VUE POST
elif st.session_state.view == 'post' and st.session_state.selected_post_idx is not None:
    sorted_acts = sorted(st.session_state.activities, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    act = sorted_acts[st.session_state.selected_post_idx]
    
    col1, col2 = st.columns([20, 1])
    with col1:
        if st.button("⬅️ Retour"):
            st.session_state.view = 'home'
            st.rerun()
    with col2:
        if st.button("❌", key="close_post"):
            st.session_state.view = 'home'
            st.rerun()
    
    # ENCADREMENT - TITRE ET INFO
    st.markdown(f"""
    <div class='publication-box'>
        <div class='pub-header'>
            <div>
                <p class='pub-title'>{act['title']}</p>
                <p class='pub-location'>📍 {act['location']}</p>
                <p class='pub-date'>📅 {act['date']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # BOUTON TELECHARGER
    if act.get("photos"):
        zip_data = create_zip_download(act["photos"], act["title"])
        st.download_button(
            label="⬇️ Télécharger toutes les photos (ZIP)",
            data=zip_data,
            file_name=f"{act['title'].replace(' ', '_')}_photos.zip",
            mime="application/zip",
            key="dl_zip"
        )
    
    # ENCADREMENT - IMAGES
    st.markdown("<div class='publication-box'>", unsafe_allow_html=True)
    
    if act.get("photos"):
        st.image(act["photos"][st.session_state.carousel_idx], use_column_width=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Précédent", use_container_width=True):
                st.session_state.carousel_idx = (st.session_state.carousel_idx - 1) % len(act["photos"])
                st.rerun()
        with col2:
            st.markdown(f"<p style='text-align: center; color: #6B7280;'>📷 {st.session_state.carousel_idx + 1} / {len(act['photos'])}</p>", unsafe_allow_html=True)
        with col3:
            if st.button("Suivant ➡️", use_container_width=True):
                st.session_state.carousel_idx = (st.session_state.carousel_idx + 1) % len(act["photos"])
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ENCADREMENT - DESCRIPTIONS
    st.markdown("<div class='publication-box'>", unsafe_allow_html=True)
    
    if act.get("image_description"):
        st.markdown(f"<p style='font-weight: 700;'>📸 Description images :</p>", unsafe_allow_html=True)
        st.markdown(act['image_description'])
    
    if act.get("description"):
        st.markdown(f"<p style='font-weight: 700;'>📝 Description :</p>", unsafe_allow_html=True)
        st.markdown(act['description'])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ENCADREMENT - LIKES
    st.markdown("<div class='publication-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"❤️ ({act.get('likes', 0)})", key="like_btn"):
            sorted_acts[st.session_state.selected_post_idx]["likes"] += 1
            st.session_state.activities = sorted_acts
            save_data(st.session_state.activities)
            st.rerun()
    with col2:
        st.markdown(f"💬 {len(act.get('comments', []))}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ENCADREMENT - FORMULAIRE COMMENTAIRE
    st.markdown("<div class='publication-box'>", unsafe_allow_html=True)
    st.subheader("💬 Ajouter commentaire")
    name = st.text_input("Nom:", key="cmt_name")
    text = st.text_input("Message:", key="cmt_text")
    
    if st.button("Publier", key="cmt_submit"):
        if name and text:
            sorted_acts[st.session_state.selected_post_idx]["comments"].append({
                "name": name,
                "text": text,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.session_state.activities = sorted_acts
            save_data(st.session_state.activities)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ENCADREMENT - COMMENTAIRES
    if act.get("comments"):
        st.markdown("<div class='publication-box'>", unsafe_allow_html=True)
        st.subheader("📌 Commentaires")
        for c in act["comments"]:
            st.markdown(f"""
            <div style='background: #F9FAFB; padding: 1rem; border-radius: 8px; margin: 0.8rem 0; border-left: 4px solid #3B82F6;'>
                <p style='margin: 0;'><b>{c['name']}</b> <span style='color: #9CA3AF; font-size: 0.85rem;'>{c['date']}</span></p>
                <p style='color: #374151; margin-top: 0.5rem;'>{c['text']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ENCADREMENT - ADMIN
    if st.session_state.is_admin:
        st.markdown("<div class='publication-box'>", unsafe_allow_html=True)
        st.subheader("🔧 Admin")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Modifier"):
                st.session_state.editing_idx = st.session_state.activities.index(act)
                st.session_state.view = 'home'
                st.rerun()
        with col2:
            if st.button("❌ Supprimer publication"):
                st.session_state.activities.remove(act)
                save_data(st.session_state.activities)
                st.session_state.view = 'home'
                st.success("✓ Supprimée!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
