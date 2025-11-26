# app.py
import os
import requests
import streamlit as st
import google.generativeai as genai

# -------------------------
# Configuration / Keys
# -------------------------
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")  # optional but recommended for posters

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in environment variables. Set it before running.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# -------------------------
# System instruction (as requested)
# -------------------------
SYSTEM_INSTRUCTIONS = """
You are a movie fan who loves spotting hidden Easter eggs, references, and fun details in films.
When someone gives you a movie or scene, give 5–10 different Easter eggs in one message, numbered or bulleted.
Each Easter egg should be concise, human-like, and enthusiastic. Use emojis naturally.
Don't repeat phrases, and keep it friendly and casual.
"""

# Gemini model for generating Easter eggs
egg_model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=SYSTEM_INSTRUCTIONS
)

# -------------------------
# CSS - Option A: Black background + film strips sides
# -------------------------
page_css = """
<style>
/* solid black background */
[data-testid="stAppViewContainer"] > div:first-child {
    background-color: #000000;
}

/* left film strip */
.film-strip-left {
    position: fixed;
    top: 0;
    left: 0;
    width: 120px;
    height: 100%;
    background-image: url('https://i.imgur.com/3F0pu7q.png');
    background-size: contain;
    background-repeat: repeat-y;
    opacity: 0.25;
    z-index: -1;
}

/* right film strip */
.film-strip-right {
    position: fixed;
    top: 0;
    right: 0;
    width: 120px;
    height: 100%;
    background-image: url('https://i.imgur.com/3F0pu7q.png');
    background-size: contain;
    background-repeat: repeat-y;
    opacity: 0.25;
    z-index: -1;
}

/* center content card */
.center-card {
    background: rgba(255,255,255,0.98);
    padding: 24px 28px;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(7,7,7,0.08);
    max-width: 880px;
    margin: 16px auto;
}

/* padding to prevent content overlapping film strips */
[data-testid="stAppViewContainer"] {
    padding-left: 140px !important;
    padding-right: 140px !important;
    padding-top: 20px;
    padding-bottom: 40px;
}

/* make poster images rounded */
img {
    border-radius: 8px;
}

/* hide film strips on small screens */
@media (max-width: 768px) {
    .film-strip-left, .film-strip-right {
        display: none;
    }
    .center-card {
        padding: 16px;
        margin: 8px;
    }
}
</style>

<div class="film-strip-left"></div>
<div class="film-strip-right"></div>
"""

st.markdown(page_css, unsafe_allow_html=True)

# -------------------------
# TMDb poster helper
# -------------------------
def tmdb_search_poster(title):
    if not TMDB_API_KEY or not title:
        return None
    try:
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": title}
        r = requests.get(search_url, params=params, timeout=8)
        if r.status_code != 200:
            return None
        data = r.json()
        if not data.get("results"):
            return None
        best = data["results"][0]
        poster_path = best.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None
    except Exception:
        return None

# -------------------------
# Gemini Easter egg helper
# -------------------------
def generate_easter_eggs(user_input):
    try:
        chat = egg_model.start_chat(history=[])
        response = chat.send_message(user_input)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error fetching Easter eggs: {e}"

# -------------------------
# Streamlit UI
# -------------------------
st.markdown('<div class="center-card">', unsafe_allow_html=True)

# header
st.markdown("<h1 style='text-align:center;margin:0;color:#222;'>🔍 Movie Easter Egg Lens</h1>", unsafe_allow_html=True)
st.markdown("")

# instructions
st.markdown("""
Ask about any movie you would like to find Easter eggs about,  
for example **Harry Potter**, **Inception**, or **Interstellar**,  
to get multiple hidden Easter eggs and fun movie secrets! 😎
""")

# examples
st.subheader("💡 Try these:")
examples = [
    "What hidden stuff is in the first Harry Potter movie?",
    "Inception's spinning top scene – any cool Easter eggs?",
    "Any fun secrets in Interstellar's tesseract scene?",
    "Quidditch scenes in Harry Potter – anything I missed?",
    "Dream layers in Inception – hidden details?",
    "Interstellar – subtle things Nolan put in the movie?"
]
for ex in examples:
    st.markdown(f"- {ex}")

st.markdown("---")

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# input
st.subheader("🎬 Ask about a movie or scene")
user_input = st.text_input("Enter movie or scene:", placeholder="e.g., 'Hidden details in Harry Potter: Quidditch scenes'")

col1, col2, col3 = st.columns([1,6,1])
with col2:
    search_btn = st.button("🔍 Find Easter Eggs")
    clear_btn = st.button("🗑️ Clear Chat")

if clear_btn:
    st.session_state.chat_history = []

if search_btn and user_input.strip():
    poster = tmdb_search_poster(user_input)
    easter_text = generate_easter_eggs(user_input)
    st.session_state.chat_history.insert(0, {
        "user": user_input,
        "assistant": easter_text,
        "poster": poster
    })

# display chat history
for item in st.session_state.chat_history:
    st.markdown("**You:**")
    st.write(item["user"])
    if item.get("poster"):
        st.image(item["poster"], width=260)
    st.markdown("**Easter Egg 🥚:**")
    st.write(item["assistant"])
    st.markdown("---")

# footer
st.markdown("""
<div style='text-align: center; color: #ccc; padding-top: 6px;'>
    <p>🎬 <strong>Movie Easter Egg Lens</strong> | Powered by 
        <a href='https://www.themoviedb.org/' target='_blank'>TMDb</a>, 
        <a href='https://ai.google.dev/' target='_blank'>Google Gemini</a>, 
        <a href='https://render.com/' target='_blank'>Render</a> &amp; 
        <a href='https://streamlit.io/' target='_blank'>Streamlit</a>
    </p>
    <p>Made with ❤️ for movie enthusiasts</p>
    <p>by <strong>Sachin Prabhu</strong></p>
    <p>🔗 <a href='https://github.com/sachinprabhu007/MovieEasterEggLens' t
