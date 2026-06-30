# Video Intelligence Agent

A system that converts videos into structured knowledge.

It takes YouTube links or MP4 files and generates:
- Transcript
- Summary
- Question-answering over content
- Persistent logs in Google Sheets

---

# Features

- YouTube URL support
- MP4 upload support
- Whisper-based transcription
- AI-style summarization
- Question answering over video content
- Google Sheets logging system
- Docker support for deployment

---

# Architecture

Video → Audio Extraction → Whisper Transcription → Text Segments → Summary → Q&A → Google Sheets Storage

---

# Tech Stack

- Python
- Whisper (Speech-to-text)
- Gradio (UI)
- yt-dlp (video download)
- Google Sheets API
- Docker

---

# Setup Instructions

## 1. Clone repository
git clone https://github.com/<your-username>/video-intelligence-agent

## 2. Install dependencies
pip install -r requirements.txt

## 3. Run application
python app.py

---

# Docker Setup

## Build image
docker build -t video-intelligence-agent .

## Run container
docker run -p 7860:7860 video-intelligence-agent

---

# Environment Variables

Create `.env` file:

GROQ_API_KEY=your_key
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_APPLICATION_CREDENTIALS=credentials.json

---

# Google Sheets Setup

Create a sheet with:

Sheet1:
- Timestamp
- Video URL
- Summary
- Transcript

QnA_Log:
- Timestamp
- Video URL
- Question
- Answer

---

# Current Limitations

- Keyword-based retrieval (not semantic yet)
- No vector database integration
- Single-video context only
- Requires stable internet for YouTube downloads

---

# Roadmap

- Add semantic embeddings
- Add vector search
- Multi-video memory system
- Authentication layer
- Cloud-native deployment

---

# Changelog

See `CHANGELOG.md` for daily development progress.

---

# License

MIT License
