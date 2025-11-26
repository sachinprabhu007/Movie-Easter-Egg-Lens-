# 🎬 Movie Easter Egg Lens 🔍

Discover hidden Easter eggs, references, and fun secrets in your favorite movies! Ask about any movie or scene and get **5–10 unique Easter eggs** generated in a human-like, enthusiastic style with emojis. Optional posters are fetched from TMDb for visual context.

---

## 🌟 Features

- Ask about any movie or scene (e.g., *Harry Potter*, *Inception*)  
- Get 5–10 unique Easter eggs in a single response  
- Human-like, casual, emoji-rich responses  
- Optional TMDb poster displayed with Easter eggs  
- Chat history maintained (newest first)  
- Black background with film strips for immersive movie vibe  
- Clear Chat option to reset history  

## 🚀 Live Demo
- Visit the live application: [https://plantnet-plant-identifier-1.onrender.com/](https://movie-easter-egg-lens.onrender.com/)

---
🖼️ Screenshots

User query with Gemini-generated Easter eggs and TMDb poster
Newest responses appear on top, posters optional

## Sequence Diagram 
<img width="1503" height="812" alt="movie easter eggs -sequence diagram v1" src="https://github.com/user-attachments/assets/566ef813-9bab-40c7-9a40-d3f19e5de3a7" />

## 🏗️ Architecture

The app combines **Streamlit**, **Google Gemini**, and **TMDb API**:

## 1️⃣ Frontend (Streamlit)

- **Framework:** [Streamlit](https://streamlit.io/)  
- **Responsibilities:**
  - Accept user queries (movie names or specific scenes)
  - Display chat history with newest responses on top
  - Show Easter Egg 🥚 responses from Google Gemini
  - Show TMDb poster images if available
  - Clear chat history
  - Footer with links to GitHub, Render, TMDb, Streamlit, and Google Gemini

- **UI Features:**
  - Black background with film strips for visual theme
  - Input textbox for queries
  - Buttons: 🔍 Find Easter Eggs & 🗑️ Clear Chat
  - Example queries displayed to guide the user

---

## 2️⃣ Backend (Render + APIs)

- **Google Gemini API**
  - `egg_model` → Generates 5–10 unique Easter eggs for a given query
  - `title_extract_model` → Extracts canonical movie title from user input

- **TMDb API**
  - Optional poster/backdrop fetch based on canonical title or raw query
  - Ensures correct image for old/new movie versions

- **Server**
  - Hosted on [Render](https://render.com/)
  - Streamlit app runs as backend and frontend together
  - Environment variables store API keys securely
    - `GOOGLE_API_KEY`
    - `TMDB_API_KEY` (optional)

---

## 3️⃣ Query Flow
User Input → Extract Canonical Title (Gemini) → Fetch Poster (TMDb) → Generate Easter Eggs (Gemini) → Display in Streamlit UI


**Step-by-Step:**

1. **User submits a query** in Streamlit (e.g., "Hidden details in Harry Potter: Quidditch scenes").
2. **Title Extraction:**  
   - `title_extract_model` attempts to parse canonical movie title.  
   - If no clear title, raw query is used for poster fetch.
3. **Poster Fetch (Optional):**  
   - TMDb API searches for poster based on title.  
   - Selects correct poster for old vs new movie versions.
4. **Generate Easter Eggs:**  
   - `egg_model` generates 5–10 unique Easter eggs in one API call.  
   - Responses are human-like, casual, and emoji-rich.
5. **Display Results:**  
   - Poster image (if available)  
   - Easter Egg 🥚 responses  
   - Chat history updates with newest query on top
6. **Footer:**  
   - Shows app credits and links to GitHub, Render, TMDb, Streamlit, and Google Gemini.

---

## 4️⃣ Deployment on Render

- **Build Command:** `pip install -r requirements.txt` (optional, Render auto-detects Python)
- **Start Command:**  ```streamlit run app.py --server.port $PORT --server.enableCORS false```
- Environment Variables: GOOGLE_API_KEY and TMDB_API_KEY
- Optional: Enable Auto-Deploy from GitHub

### Environment Variables:

- GOOGLE_API_KEY - Google Gemini API key
- TMDB_API_KEY - TMDb API key (optional)
- Optional: Enable Auto-Deploy from GitHub to automatically update on pushes.

**Components:**

1. **Streamlit UI**
   - Input box for user queries  
   - Buttons: 🔍 Find Easter Eggs & 🗑️ Clear Chat  
   - Chat display: user input + Easter Egg 🥚 response + poster  
   - Footer with links  

2. **Google Gemini API**
   - `title_extract_model` → Extracts canonical movie titles  
   - `egg_model` → Generates 5–10 Easter eggs in human style  

3. **TMDb API**
   - Fetches posters/backdrops for visual context  
   - Optional; works if a valid TMDb API key is provided  

4. **Session State**
   - Stores chat history (newest queries appear on top)  

---

## 💡 Try These Examples

- What hidden stuff is in the first Harry Potter movie?  
- Inception's spinning top scene – any cool Easter eggs?  
- Any fun secrets in Interstellar's tesseract scene?  
- Quidditch scenes in Harry Potter – anything I missed?  
- Dream layers in Inception – hidden details?  
- Interstellar – subtle things Nolan put in the movie?  

---

## 🛠️ Installation

1. Clone the repository:

git clone https://github.com/sachinprabhu007/MovieEasterEggLens.git
cd MovieEasterEggLens

2. Install dependencies:
pip install -r requirements.txt

3. Set environment variables in Render environment :

```
export GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"
export TMDB_API_KEY="YOUR_TMDB_API_KEY"  # Optional for posters
```
--- 
### 🔑 API Keys
TMDb API

- Sign up: https://www.themoviedb.org/signup
- Apply for API key: Settings → API
- Documentation: Search Movie API

Google Gemini

- Get free API key: https://makersuite.google.com/app/apikey
- Documentation: Google Generative AI

--- 
### 💻 Usage


- Type your query (e.g., "Hidden details in Harry Potter: Quidditch scenes")
- Click 🔍 Find Easter Eggs
- View the Easter Egg 🥚 responses and poster image
- Use 🗑️ Clear Chat to reset history

--- 


📦 Dependencies

- streamlit
- requests
- google-generativeai

## 📄 License

Please go through [LICENSE](LICENSE) file for details.

