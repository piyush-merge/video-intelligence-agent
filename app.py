import gradio as gr
import yt_dlp
import whisper
from datetime import datetime

# -----------------------
# OPTIONAL STORAGE (HF SAFE)
# -----------------------
SHEETS_ENABLED = False
video_sheet = None
qa_sheet = None

print("Sheets disabled (Hugging Face environment)")

# -----------------------
# MODEL
# -----------------------
model = whisper.load_model("tiny")

current_url = None

# -----------------------
# AUDIO EXTRACTION
# -----------------------
def get_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return file_path


# -----------------------
# TRANSCRIBE
# -----------------------
def transcribe(audio_path):
    return model.transcribe(audio_path)


# -----------------------
# SUMMARY (placeholder)
# -----------------------
def summarize(text):
    return f"Summary:\n{text[:500]}"


# -----------------------
# SAVE (SAFE NO-OP)
# -----------------------
def save_video(url, summary, transcript):
    print("Save skipped (no DB configured)")


def log_qa(url, question, answer):
    print("QnA log skipped (no DB configured)")


# -----------------------
# PIPELINE
# -----------------------
def process_video(url):
    global current_url
    current_url = url

    audio = get_audio(url)
    result = transcribe(audio)

    text = result.get("text", "")
    segments = result.get("segments", [])

    summary = summarize(text)

    save_video(url, summary, text)

    return summary, text[:2000], segments


# -----------------------
# Q&A ENGINE
# -----------------------
def answer_question(question, segments):
    if not segments:
        return "No transcript available."

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
