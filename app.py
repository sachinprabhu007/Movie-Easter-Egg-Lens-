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
# System instruction (exact as requested)
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

# A small helper model/prompt for extracting canonical movie titles (keeps it concise)
# This is intentionally minimal and separate from the main SYSTEM_INSTRUCTIONS.
title_extract_model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
You are a helpful assistant. When given a user's query, if it clearly refers to a specific movie (including fuzzy references like "2nd Harry Potter movie", "Harry Potter 2", "first Matrix film", etc.), respond with the movie's canonical title only (e.g., "Harry Potter and the Chamber of Secrets"). 
If the input does not clearly refer to a single movie title, respond with an empty string.
Respond with only the title or an empty string, nothing else.
"""
)

# -------------------------
# Helper: TMDb poster fetch using a title (if available)
# -------------------------
def tmdb_search_poster(title):
    """
    Search TMDb for the best match poster for a given title.
    Returns poster_url or None.
    """
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
        # take first result
        best = data["results"][0]
        poster_path = best.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None
    except Exception:
        return None

# -------------------------
# Helper: try to extract canonical movie title using Gemini
# -------------------------
def extract_canonical_title(user_input):
    """
    Use a short Gemini prompt to extract a canonical movie title if present.
    Returns a title string or None/empty.
    """
    try:
        chat = title_extract_model.start_chat(history=[])
        resp = chat.send_message(user_input)
        title = resp.text.strip()
        # if model returns nothing or not helpful, treat as no title
        if not title:
            return None
        # Some safety: if response looks too long, skip
        if len(title) > 120:
            return None
        return title
    except Exception:
        return None

# -------------------------
# Helper: generate Easter eggs (single Gemini call)
# -------------------------
def generate_easter_eggs(user_input):
    """
    Call Gemini once to produce 5-10 Easter eggs for the user's input.
    Returns string text (the assistant output).
    """
    try:
        chat = egg_model.start_chat(history=[])
        response = chat.send_message(user_input)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error fetching Easter eggs: {e}"

# -------------------------
# Streamlit UI
# -------------------------

# header
st.markdown("<h1 style='text-align:center;margin:0;'>🔍 Movie Easter Egg Lens</h1>", unsafe_allow_html=True)
st.markdown("")  # spacing

# instructions (exact text you asked for)
st.markdown("""
Ask about any movie you would like to find Easter eggs about,  
for example **Harry Potter**, **Inception**, or **Interstellar**,  
to get multiple hidden Easter eggs and fun movie secrets! 😎
""")

st.markdown("")

# examples (exact list, one per line)
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

# initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# input area
st.subheader("🎬 Ask about a movie or scene")
user_input = st.text_input("Enter movie or scene:", placeholder="e.g., 'Hidden details in Harry Potter: Quidditch scenes'")

col1, col2, col3 = st.columns([1, 6, 1])  # just for nicer layout of button area
with col2:
    search_btn = st.button("🔍 Find Easter Eggs")
    clear_btn = st.button("🗑️ Clear Chat")

# handle clear
if clear_btn:
    st.session_state.chat_history = []

# handle search click
if search_btn and user_input.strip():
    # 1) Ask Gemini to extract canonical title (if any)
    canonical_title = extract_canonical_title(user_input)
    # 2) Try TMDb poster fetch using the canonical title (if found), else try using the raw input
    poster = None
    if canonical_title:
        poster = tmdb_search_poster(canonical_title)
    # if no poster found yet, try searching using raw user input (useful if user typed exact title)
    if not poster:
        poster = tmdb_search_poster(user_input)

    # 3) Call Gemini once to generate Easter eggs (use original user_input so scene queries remain accurate)
    easter_text = generate_easter_eggs(user_input)

    # 4) Insert newest at top
    st.session_state.chat_history.insert(0, {
        "user": user_input,
        "assistant": easter_text,
        "poster": poster,
        "title_hint": canonical_title or ""
    })

# -------------------------
# Display chat history (newest first)
# -------------------------
for item in st.session_state.chat_history:
    # You (user)
    st.markdown("**You:**")
    st.write(item["user"])

    # Poster (if available)
    if item.get("poster"):
        st.image(item["poster"], width=260)

    # Assistant label
    st.markdown("**Easter Egg 🥚:**")
    # Easter eggs response (already a block of text with bullets/numbering as provided by Gemini)
    st.write(item["assistant"])
    st.markdown("---")

# footer inside center card
st.markdown("""
<div style='text-align: center; color: #666; padding-top: 6px;'>
    <p>🎬 <strong>Movie Easter Egg Lens</strong> | Powered by 
        <a href='https://www.themoviedb.org/' target='_blank'>TMDb</a>, 
        <a href='https://ai.google.dev/' target='_blank'>Google Gemini</a>, 
        <a href='https://render.com/' target='_blank'>Render</a> &amp; 
        <a href='https://streamlit.io/' target='_blank'>Streamlit</a>
    </p>
    <p>Made with ❤️ for movie enthusiasts</p>
    <p>by <strong>Sachin Prabhu</strong></p>
    <p>🔗 <a href='https://github.com/sachinprabhu007/MovieEasterEggLens' target='_blank'>View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close center-card div
