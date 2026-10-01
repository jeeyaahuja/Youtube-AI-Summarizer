# 🎥 Youtube-AI-Summarizer

An AI-powered web application built with **Streamlit** and **Google Gemini AI** that converts YouTube videos into concise bullet points, clear explanations, or step-by-step teaching notes in multiple languages.

Upgraded with **Production Map-Reduce Chunking**, **Multi-Level Subtitle Fallbacks**, and **Session Caching**!

---

## ✨ Features

- 🧩 **Smart Map-Reduce Pipeline**:
  - **Single-Pass Mode ($\le$ 5,000 words)**: Fast, direct summarization for short-to-medium videos.
  - **Map-Reduce Mode ($>$ 5,000 words)**: Automatically divides long transcripts into 5,000-word segments (~30 mins of speech), summarizes each section in the *Map Phase*, and aggregates them in the *Reduce Phase* to eliminate hallucinations and context loss.
- 🔄 **Multi-Level Subtitle Fallback Engine**:
  - Automatically fetches manual captions, auto-generated subtitles, or foreign language tracks so video processing never fails.
- ⚡ **Cached & Rate-Limit Optimized**:
  - Session caching via `@st.cache_data` for instant responses (0.1s) on repeated requests with zero API token waste.
  - Built-in rate throttle safety to respect Gemini's free-tier rate limits.
- 🎯 **Multiple Summary Modes**:
  - **Bullet Points**: Key insights & main takeaways (max 200 words).
  - **Explain**: Simplified breakdown of complex concepts.
  - **Teach**: Beginner-friendly, step-by-step educational guide.
- 🌐 **Multi-Language Support**: Generate summaries in **English, Hindi, Spanish, French, or German**.
- 🖼️ **Instant Preview & Export**: Displays video thumbnail preview and provides a 1-click `.txt` download button.

---

## 🛠️ Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **LLM Engine**: [Google Generative AI (Gemini 2.5 Flash / Flash Lite)](https://ai.google.dev/)
- **Transcript Extraction**: [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
- **Environment Management**: `python-dotenv`

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Clone the Repository
```bash
git clone https://github.com/jeeyaahuja/Youtube-AI-Summarizer.git
cd Youtube-AI-Summarizer
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
