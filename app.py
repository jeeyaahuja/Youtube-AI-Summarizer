import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(
    page_title="YouTube AI Summarizer",
    layout="wide"
)
# Load env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

import time

# ---------------- FUNCTIONS ---------------- #

@st.cache_data(show_spinner=False)
def extract_transcript_details(youtube_video_url, lang_code):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]

        # 1. Direct fetch (manual & standard captions)
        try:
            api = YouTubeTranscriptApi()
            fetched = api.fetch(video_id, languages=[lang_code, 'en', 'en-US'])
        except Exception:
            # 2. Fallback: Search all manual & auto-generated tracks
            try:
                transcript_list = api.list(video_id)
            except Exception:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            try:
                t_obj = transcript_list.find_transcript([lang_code, 'en', 'en-US'])
            except Exception:
                try:
                    t_obj = transcript_list.find_generated_transcript([lang_code, 'en', 'en-US'])
                except Exception:
                    t_obj = next(iter(transcript_list))

            fetched = t_obj.fetch()

        transcript = ""
        for snippet in fetched:
            text = snippet['text'] if isinstance(snippet, dict) else getattr(snippet, 'text', str(snippet))
            transcript += " " + text

        return transcript

    except Exception:
        return None


def chunk_text(text, max_words=5000):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i : i + max_words]))
    return chunks


@st.cache_data(show_spinner=False)
def generate_gemini_content(transcript_text, summary_type, language):
    
    # Model selection
    if summary_type == "Teach":
        model = genai.GenerativeModel("gemini-2.5-flash")
    else:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")

    base_prompt = f"""
You are an expert AI assistant.

IMPORTANT:
- Output MUST be in {language}
- Be clear and structured
"""

    if summary_type == "Bullet Points":
        format_prompt = """
Mode: Bullet Points

- Give key insights in bullet points
- Keep it short and crisp
- Max 200 words
"""

    elif summary_type == "Explain":
        format_prompt = """
Mode: Explain

- Explain the content clearly
- Break down concepts simply
- Use easy language
"""

    elif summary_type == "Teach":
        format_prompt = """
Mode: Teach

- Teach like a teacher
- Start from basics
- Explain step-by-step
- Make it beginner friendly
"""

    words = transcript_text.split()
    max_words_per_chunk = 5000

    if len(words) <= max_words_per_chunk:
        final_prompt = base_prompt + format_prompt + "\n\nTranscript:\n" + transcript_text
        response = model.generate_content(final_prompt)
        return response.text
    else:
        # Map-Reduce for long transcripts (> 30 mins)
        chunks = chunk_text(transcript_text, max_words=max_words_per_chunk)
        chunk_summaries = []

        # Map Phase
        for idx, chunk in enumerate(chunks):
            map_prompt = (
                f"Summarize section {idx+1}/{len(chunks)} of this video transcript concisely:\n\n{chunk}"
            )
            chunk_resp = model.generate_content(map_prompt)
            chunk_summaries.append(f"--- Section {idx+1} Summary ---\n{chunk_resp.text}")
            time.sleep(2) # 2s sleep to safely respect API rate limits

        combined_summaries = "\n\n".join(chunk_summaries)

        # Reduce Phase
        reduce_prompt = (
            base_prompt + format_prompt +
            f"\n\nHere are summaries of different sections of a long video ({len(chunks)} sections total).\n"
            f"Combine them into a single, cohesive, non-repetitive final output:\n\n"
            + combined_summaries
        )
        response = model.generate_content(reduce_prompt)
        return response.text


# ---------------- UI ---------------- #

st.markdown("## 🎥 YouTube AI Summarizer")
st.caption("Convert videos into bullet points, explanations, or teaching notes 🚀")

st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    youtube_link = st.text_input("🔗 Enter YouTube Video Link:")

with col2:
    summary_type = st.selectbox(
        " Mode",
        ["Bullet Points", "Explain", "Teach"]
    )

    language = st.selectbox(
        " Language",
        ["English", "Hindi", "Spanish", "French", "German"]
    )


language_map = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

# ---------------- VIDEO PREVIEW ---------------- #

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[1].split("&")[0]
        st.image(
            f"http://img.youtube.com/vi/{video_id}/0.jpg",
            caption="Video Preview",
            use_container_width=True
        )
    except:
        st.warning("Invalid YouTube URL")


# ---------------- BUTTON ---------------- #

generate = st.button(" Generate Output")

if generate:
    if youtube_link:
        lang_code = language_map[language]

        with st.spinner("⏳ Processing video..."):
            transcript_text = extract_transcript_details(youtube_link, lang_code)

        if transcript_text:

            with st.spinner("🤖 Generating AI output..."):
                summary = generate_gemini_content(
                    transcript_text,
                    summary_type,
                    language
                )

            st.divider()
            st.markdown("##  Output")
            st.write(summary)

            st.download_button(
                "📥 Download",
                summary,
                file_name="summary.txt"
            )

        else:
            st.error("❌ Could not fetch transcript")

    else:
        st.warning("⚠️ Please enter a YouTube link")



# import streamlit as st
# from dotenv import load_dotenv
# import os
# import tempfile
# import google.generativeai as genai
# from youtube_transcript_api import YouTubeTranscriptApi
# import yt_dlp
# from faster_whisper import WhisperModel
# import imageio_ffmpeg
# ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

# st.set_page_config(
#     page_title="YouTube AI Summarizer",
#     layout="wide"
# )
# # Load env
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # ---------------- WHISPER MODEL (loaded once) ---------------- #

# @st.cache_resource
# def load_whisper_model():
#     return WhisperModel("small", device="cpu", compute_type="int8")


# # ---------------- FUNCTIONS ---------------- #

# def extract_transcript_details(youtube_video_url, lang_code):
#     try:
#         video_id = youtube_video_url.split("v=")[1].split("&")[0]

#         api = YouTubeTranscriptApi()
#         fetched = api.fetch(video_id, languages=[lang_code, 'en'])

#         transcript = ""
#         for snippet in fetched:
#             transcript += " " + snippet.text

#         return transcript

#     except:
#         return None


# def download_audio(youtube_video_url, out_dir):
#     out_path = os.path.join(out_dir, "audio.%(ext)s")
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": out_path,
#         "postprocessors": [{
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": "mp3",
#         }],
#         "ffmpeg_location": ffmpeg_path,
#         "quiet": True,
#         "no_warnings": True,
#         "socket_timeout": 30,
#         "retries": 5,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([youtube_video_url])

#     for f in os.listdir(out_dir):
#         if f.startswith("audio."):
#             return os.path.join(out_dir, f)
#     return None


# def transcribe_with_whisper(youtube_video_url):
#     model = load_whisper_model()
#     with tempfile.TemporaryDirectory() as tmp_dir:
#         audio_path = download_audio(youtube_video_url, tmp_dir)
#         if not audio_path:
#             return None

#         segments, _ = model.transcribe(audio_path, beam_size=5)
#         transcript = " ".join(seg.text for seg in segments)
#         return transcript.strip()


# def generate_gemini_content(transcript_text, summary_type, language):
    
#     # Model selection
#     if summary_type == "Teach":
#         model = genai.GenerativeModel("gemini-2.5-flash")
#     else:
#         model = genai.GenerativeModel("gemini-2.5-flash-lite")

#     base_prompt = f"""
# You are an expert AI assistant.

# IMPORTANT:
# - Output MUST be in {language}
# - Be clear and structured
# """

#     if summary_type == "Bullet Points":
#         format_prompt = """
# Mode: Bullet Points

# - Give key insights in bullet points
# - Keep it short and crisp
# - Max 200 words
# """

#     elif summary_type == "Explain":
#         format_prompt = """
# Mode: Explain

# - Explain the content clearly
# - Break down concepts simply
# - Use easy language
# """

#     elif summary_type == "Teach":
#         format_prompt = """
# Mode: Teach

# - Teach like a teacher
# - Start from basics
# - Explain step-by-step
# - Make it beginner friendly
# """

#     final_prompt = base_prompt + format_prompt + "\n\nTranscript:\n" + transcript_text

#     response = model.generate_content(final_prompt)
#     return response.text


# # ---------------- UI ---------------- #

# st.markdown("## 🎥 YouTube AI Summarizer")
# st.caption("Convert videos into bullet points, explanations, or teaching notes 🚀")

# st.divider()

# col1, col2 = st.columns([3, 1])

# with col1:
#     youtube_link = st.text_input("🔗 Enter YouTube Video Link:")

# with col2:
#     summary_type = st.selectbox(
#         " Mode",
#         ["Bullet Points", "Explain", "Teach"]
#     )

#     language = st.selectbox(
#         " Language",
#         ["English", "Hindi", "Spanish", "French", "German"]
#     )


# language_map = {
#     "English": "en",
#     "Hindi": "hi",
#     "Spanish": "es",
#     "French": "fr",
#     "German": "de"
# }

# # ---------------- VIDEO PREVIEW ---------------- #

# if youtube_link:
#     try:
#         video_id = youtube_link.split("v=")[1].split("&")[0]
#         st.image(
#             f"http://img.youtube.com/vi/{video_id}/0.jpg",
#             caption="Video Preview",
#             use_container_width=True
#         )
#     except:
#         st.warning("Invalid YouTube URL")


# # ---------------- BUTTON ---------------- #

# generate = st.button(" Generate Output")

# if generate:
#     if youtube_link:
#         lang_code = language_map[language]

#         with st.spinner("🎙️ Transcribing audio locally (forced test)..."):
#          transcript_text = transcribe_with_whisper(youtube_link)

#         if transcript_text:

#             with st.spinner("🤖 Generating AI output..."):
#                 summary = generate_gemini_content(
#                     transcript_text,
#                     summary_type,
#                     language
#                 )

#             st.divider()
#             st.markdown("##  Output")
#             st.write(summary)

#             st.download_button(
#                 "📥 Download",
#                 summary,
#                 file_name="summary.txt"
#             )

#         else:
#             st.error("❌ Could not fetch transcript")

#     else:
#         st.warning("⚠️ Please enter a YouTube link")