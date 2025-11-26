import streamlit as st
import google.generativeai as genai
import os

# -----------------------------
# Configure Gemini API key
# -----------------------------
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error(
        "❌ GOOGLE_API_KEY not found in environment variables. "
        "Set it in Render or your system before running the app."
    )
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# -----------------------------
# Gemini model
# -----------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
You are a movie fan who loves spotting hidden Easter eggs, references, and fun details in films.
When someone gives you a movie or scene, give 5–10 different Easter eggs in one message, numbered or bulleted.
Each Easter egg should be concise, human-like, and enthusiastic. Use emojis naturally.
Don't repeat phrases, and keep it friendly and casual.
"""
)

# -----------------------------
# Function to query Gemini once
# -----------------------------
def find_easter_eggs(movie_query):
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(movie_query)
        return response.text
    except Exception as e:
        return f"❌ Oops, something went wrong: {str(e)}"

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Easter Egg Lens", page_icon="🎬")
st.title("🎬 Movie Easter Egg Lens 🔍")
st.markdown(
    "Ask about any movie you would like to find Easter eggs about, "
    "for example **Harry Potter**, **Inception**, or **Interstellar**, "
    "to get multiple hidden Easter eggs and fun movie secrets! 😎"
)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
movie_query = st.text_input(
    "Enter a movie or scene:",
    placeholder="e.g., 'Hidden details in Harry Potter: Quidditch scenes'"
)

# Submit button
if st.button("🔍 Find Easter Eggs"):
    if movie_query.strip():
        st.info("🎬 Digging for hidden Easter eggs...")
        response = find_easter_eggs(movie_query)
        st.session_state.chat_history.append((movie_query, response))

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# Display chat history (most recent first)
for human, bot in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {human}")
    st.markdown(f"**Easter Egg 🥚:** {bot}")
    st.markdown("---")

# -----------------------------
# Example prompts
# -----------------------------
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

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎬 <strong>Movie Easter Egg Lens</strong> | Powered by 
        <a href='https://makersuite.google.com/' target='_blank'>Gemini API</a>, 
        <a href='https://render.com/' target='_blank'>Render</a> & 
        <a href='https://streamlit.io/' target='_blank'>Streamlit</a>
    </p>
    <p>Made with ❤️ for movie enthusiasts</p>
    <p>by Sachin Prabhu</p>
    <p>🔗 <a href='https://github.com/sachinprabhu007/movie-easter-egg-lens' target='_blank'>View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
