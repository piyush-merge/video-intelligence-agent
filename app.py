import gradio as gr
import yt_dlp
import whisper
from datetime import datetime
import gspread

SHEETS_ENABLED = True

try:
    from google.auth import default

    creds, _ = default()
    gc = gspread.authorize(creds)

    SHEET_ID = "YOUR_SHEET_ID"

    sh = gc.open_by_key(SHEET_ID)
    video_sheet = sh.worksheet("Sheet1")
    qa_sheet = sh.worksheet("QnA_Log")

except Exception as e:
    print("Google Sheets disabled (HF environment):", e)
    SHEETS_ENABLED = False
    video_sheet = None
    qa_sheet = None

# -----------------------
# MODEL
# -----------------------
model = whisper.load_model("tiny")

current_url = None


# -----------------------
# AUDIO EXTRACTION
# -----------------------
def get_audio(url):
    import os

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)

    return file


# -----------------------
# TRANSCRIBE
# -----------------------
def transcribe(audio_path):
    return model.transcribe(audio_path)


# -----------------------
# SUMMARY (simple placeholder)
# -----------------------
def summarize(text):
    return f"Summary:\n{text[:500]}"


# -----------------------
# SAVE TO SHEETS
# -----------------------
def save_video(url, summary, transcript):
    if video_sheet is None:
        print("Sheets disabled: video log skipped")
        return

    video_sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        url,
        summary,
        transcript[:3000]
    ])


def log_qa(url, question, answer):
    if qa_sheet is None:
        print("Sheets disabled: QnA log skipped")
        return

    qa_sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        url,
        question,
        answer
    ])

# -----------------------
# PIPELINE
# -----------------------
def process_video(url):
    global current_url
    current_url = url

    audio = get_audio(url)
    result = transcribe(audio)

    text = result["text"]
    segments = result.get("segments", [])

    summary = summarize(text)

    save_video(url, summary, text)

    return summary, text[:2000], segments


# -----------------------
# Q&A
# -----------------------
def answer_question(question, segments):
    context = " ".join([s.get("text", "") for s in segments])

    return context[:1000]


def qa_interface(question, segments):
    answer = answer_question(question, segments)
    log_qa(current_url, question, answer)
    return answer


# -----------------------
# UI
# -----------------------
with gr.Blocks() as app:

    gr.Markdown("# Video Intelligence Agent")

    url = gr.Textbox(label="YouTube URL")
    btn = gr.Button("Process Video")

    summary = gr.Textbox(label="Summary")
    transcript = gr.Textbox(label="Transcript")
    segments_state = gr.State()

    btn.click(
        process_video,
        inputs=url,
        outputs=[summary, transcript, segments_state]
    )

    question = gr.Textbox(label="Ask Question")
    ask = gr.Button("Ask")
    answer = gr.Textbox(label="Answer")

    ask.click(
        qa_interface,
        inputs=[question, segments_state],
        outputs=answer
    )

app.launch()
