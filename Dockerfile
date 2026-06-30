FROM python:3.10

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y ffmpeg git

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose Gradio port
EXPOSE 7860

# Run app
CMD ["python", "app.py"]
