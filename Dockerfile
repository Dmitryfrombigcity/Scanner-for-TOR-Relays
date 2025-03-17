# syntax=docker/dockerfile:1-labs
FROM python:3.12.9-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY --exclude=pyproject.toml \
    --exclude=poetry.lock \
    --exclude=requirements.txt . .

RUN adduser --no-create-home app \
    && chown -R app /app
USER app

ENTRYPOINT ["python", "main.py"]
