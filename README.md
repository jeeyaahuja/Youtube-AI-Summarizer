# 🎥 Youtube-AI-Summarizer

An AI-powered web application built with Streamlit and Google Gemini that converts YouTube videos into concise bullet points, clear explanations, or beginner-friendly teaching notes in multiple languages.

---

## ✨ Features

- **Multiple Summary Modes**:
  - **Bullet Points**: Get key takeaways quickly (max 200 words).
  - **Explain**: Simplified breakdown of complex concepts.
  - **Teach**: Beginner-friendly, step-by-step educational notes.
- **Multi-Language Support**: Generate summaries in English, Hindi, Spanish, French, or German.
- **Instant Video Preview**: View the YouTube video thumbnail directly in the interface.
- **Downloadable Summaries**: Easily export generated summaries as `.txt` files.

---

## 🛠️ Tech Stack

- **Frontend / Framework**: [Streamlit](https://streamlit.io/)
- **LLM Engine**: [Google Generative AI (Gemini 2.5 Flash / Flash Lite)](https://ai.google.dev/)
- **Transcript Extraction**: [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
- **Environment Management**: `python-dotenv`

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Clone the Repository
```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/Youtube-AI-Summarizer.git
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
Create a `.env` file in the root directory and add your Gemini API key:
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
