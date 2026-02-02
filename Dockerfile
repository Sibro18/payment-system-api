FROM python:3.13.5-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN mv docker/entrypoint.sh /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
