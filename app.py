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
# Initialize Gemini model
# -----------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
You are a huge movie fan. Talk like a human who loves spotting cool Easter eggs and hidden details in movies. 
Be casual, enthusiastic, short, and fun. Use emojis where it fits. 
Keep it like you're chatting with a friend about movies.
"""
)

# -----------------------------
# Function to query Gemini
# -----------------------------
def find_easter_eggs(user_query, chat_history=[]):
    try:
        chat = model.start_chat(history=[])
        for human, assistant in chat_history:
            chat.send_message(human)
        response = chat.send_message(user_query)
        return response.text
    except Exception as e:
        return f"❌ Oops, something went wrong: {str(e)}"

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Easter Egg Lens", page_icon="🎬")
st.title("🎬 Movie Easter Egg Lens 🥚")
st.markdown(
    "Ask about **Harry Potter**, **Inception**, or **Interstellar** and I'll spill all the hidden Easter eggs and fun movie secrets! 😎"
)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input(
    "Ask me anything about the movies:",
    placeholder="e.g., 'Any hidden details in Harry Potter's Quidditch scenes?'"
)

# Submit button
if st.button("🔍 Find Easter Eggs"):
    if user_input.strip():
        response = find_easter_eggs(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append((user_input, response))

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# Display chat history in a friendly way
for human, bot in st.session_state.chat_history:
    st.markdown(f"**You:** {human}")
    st.markdown(f"**Movie Fan:** {bot}")
    st.markdown("---")

# -----------------------------
# Example prompts
# -----------------------------
st.subheader("💡 Try these questions:")
examples = [
    "What hidden stuff is in the first Harry Potter movie?",
    "Inception's spinning top scene – any cool Easter eggs?",
    "Any fun secrets in Interstellar's tesseract scene?",
    "Quidditch scenes in Harry Potter – anything I missed?",
    "Dream layers in Inception – hidden details?",
    "Interstellar – subtle things Nolan put in the movie?"
]
st.write(", ".join(examples))
