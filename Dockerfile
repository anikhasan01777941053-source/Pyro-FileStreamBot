FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python3 fix_session.py; echo 'FIX DONE'; python3 -m WebStreamer; echo 'WEBSTREAMER EXITED'"]
