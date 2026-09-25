FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/

# roda sem privilégio de root
RUN useradd --create-home --shell /usr/sbin/nologin chatbot \
    && chown -R chatbot:chatbot /app
USER chatbot

EXPOSE 8000

CMD ["uvicorn", "bot.main:app", "--host", "0.0.0.0", "--port", "8000"]
