import streamlit as st
import json
import os
from datetime import datetime
import base64

st.set_page_config(page_title="Mon Road Trip en Italie", page_icon="✈️", layout="wide")

st.markdown("""
<style>
body { background-color: #F9FAFB !important; }
.header { padding: 3rem; border-radius: 10px; text-align: center; margin-bottom: 2rem; background-size: cover; background-position: center; min-height: 280px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }
.header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.35); z-index: 1; }
.header h1, .header p { position: relative; z-index: 2; color: white; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); margin: 0; }
.post-card { background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #E5E7EB; text-align: center; }
.post-card p { margin: 0.5rem 0 0 0; }
.program-box { background: white; border-radius: 10px; padding: 1.5rem; text-align: center; font-size: 0.9rem; line-height: 1.8; color: #374151; }
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
        pw = st.text_input("Mot de passe:", type="password")
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
        with st.form("header_form"):
            title = st.text_input("Titre:", s.get("title"))
            subtitle = st.text_area("Sous-titre:", s.get("subtitle"), height=60)
            color = st.color_picker("Couleur texte:", s.get("text_color"))
            img = st.file_uploader("Image fond:", type=["jpg", "jpeg", "png", "webp"], key="himg")
            
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
            txt = st.text_area("Texte:", s.get("actu_text", ""), height=80)
            if st.button("Sauvegarder texte"):
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
        else:
            a = None
        
        with st.form("post_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Titre:", value=a["title"] if a else "")
                loc = st.text_input("Localisation:", value=a["location"] if a else "")
            with col2:
                d = st.date_input("Date:", value=datetime.strptime(a["date"], "%Y-%m-%d").date() if a else datetime.now())
            
            desc = st.text_area("Description:", value=a["description"] if a else "", height=80)
            
            st.subheader("📸 Photos")
            files = st.file_uploader("Photos:", accept_multiple_files=True, type=["jpg", "jpeg", "png", "gif", "webp"])
            
            photos = []
            if a and a.get("photos"):
                for i in range(len(a["photos"])):
                    col1, col2 = st.columns([4, 1])
                    with col2:
                        if st.button("❌", key=f"del_{i}"):
                            a["photos"].pop(i)
                            save_data(st.session_state.activities)
                            st.rerun()
            
            if files:
                for f in files:
                    photos.append(f"data:{f.type};base64,{base64.b64encode(f.read()).decode()}")
            
            url = st.text_input("Ou URL:")
            if url:
                photos.append(url)
            
            img_desc = st.text_area("Description images:", value=a["image_description"] if a else "", height=60)
            
            col1, col2 = st.columns(2)
            with col1:
                sub = st.form_submit_button("✓ " + ("Mettre à jour" if a else "Publier"), use_container_width=True)
            with col2:
                if a and st.form_submit_button("Annuler", use_container_width=True):
                    st.session_state.editing_idx = None
                    st.rerun()
            
            if sub:
                if title and loc:
                    if a:
                        st.session_state.activities[st.session_state.editing_idx]["title"] = title
                        st.session_state.activities[st.session_state.editing_idx]["location"] = loc
                        st.session_state.activities[st.session_state.editing_idx]["date"] = str(d)
                        st.session_state.activities[st.session_state.editing_idx]["description"] = desc
                        st.session_state.activities[st.session_state.editing_idx]["image_description"] = img_desc
                        if photos:
                            st.session_state.activities[st.session_state.editing_idx]["photos"].extend(photos)
                        save_data(st.session_state.activities)
                        st.session_state.editing_idx = None
                        st.rerun()
                    else:
                        if photos:
                            st.session_state.activities.append({
                                "id": datetime.now().timestamp(),
                                "title": title,
                                "location": loc,
                                "date": str(d),
                                "description": desc,
                                "photos": photos,
                                "image_description": img_desc,
                                "likes": 0,
                                "comments": []
                            })
                            save_data(st.session_state.activities)
                            st.success("✓")
                            st.rerun()
                        else:
                            st.error("Ajouter photo")
                else:
                    st.error("Remplir")
    
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
    
    if st.button("⬅️ Retour"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.header(act["title"])
    st.markdown(f"📍 **{act['location']}** | 📅 {act['date']}")
    
    # IMAGES
    if act.get("photos"):
        st.image(act["photos"][st.session_state.carousel_idx], use_column_width=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Précédent"):
                st.session_state.carousel_idx = (st.session_state.carousel_idx - 1) % len(act["photos"])
                st.rerun()
        with col2:
            st.markdown(f"<p style='text-align: center; color: #6B7280;'>📷 {st.session_state.carousel_idx + 1} / {len(act['photos'])}</p>", unsafe_allow_html=True)
        with col3:
            if st.button("Suivant ➡️"):
                st.session_state.carousel_idx = (st.session_state.carousel_idx + 1) % len(act["photos"])
                st.rerun()
        
        # MINIATURES
        if len(act["photos"]) > 1:
            st.write("")
            cols = st.columns(min(6, len(act["photos"])))
            for i, photo in enumerate(act["photos"]):
                with cols[i]:
                    if st.button(f"📷 {i+1}", key=f"thumb_{i}", use_container_width=True):
                        st.session_state.carousel_idx = i
                        st.rerun()
    
    if act.get("image_description"):
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%); padding: 1rem; border-radius: 10px; margin: 1.5rem 0; border-left: 4px solid #3B82F6;'>
            <p style='font-weight: 700; color: #1F2937; margin: 0;'>Description :</p>
            <p style='color: #374151; margin-top: 0.5rem;'>{act['image_description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if act.get("description"):
        st.write(act["description"])
    
    st.markdown("---")
    
    # LIKES ET COMMENTAIRES
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"❤️ ({act.get('likes', 0)})"):
            sorted_acts[st.session_state.selected_post_idx]["likes"] += 1
            st.session_state.activities = sorted_acts
            save_data(st.session_state.activities)
            st.rerun()
    with col2:
        st.write(f"💬 {len(act.get('comments', []))}")
    
    st.subheader("Commentaire")
    name = st.text_input("Nom:")
    text = st.text_input("Message:")
    
    if st.button("Publier"):
        if name and text:
            sorted_acts[st.session_state.selected_post_idx]["comments"].append({
                "name": name,
                "text": text,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.session_state.activities = sorted_acts
            save_data(st.session_state.activities)
            st.rerun()
    
    if act.get("comments"):
        st.subheader("Commentaires")
        for c in act["comments"]:
            st.markdown(f"""
            <div style='background: white; padding: 1rem; border-radius: 8px; margin: 0.8rem 0; border: 1px solid #E5E7EB;'>
                <p style='margin: 0;'><b>{c['name']}</b> <span style='color: #9CA3AF; font-size: 0.85rem;'>{c['date']}</span></p>
                <p style='color: #374151; margin-top: 0.5rem;'>{c['text']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ADMIN
    if st.session_state.is_admin:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Modifier"):
                st.session_state.editing_idx = st.session_state.activities.index(act)
                st.session_state.view = 'home'
                st.rerun()
        with col2:
            if st.button("🗑️ Supprimer"):
                st.session_state.activities.remove(act)
                save_data(st.session_state.activities)
                st.session_state.view = 'home'
                st.success("✓")
                st.rerun()
