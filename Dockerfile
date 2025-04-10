# syntax=docker/dockerfile:1-labs
FROM python:3.13.3-alpine3.21
LABEL version="2.0"
WORKDIR /app


ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

COPY --exclude=pyproject.toml \
    --exclude=poetry.lock \
    --exclude=requirements.txt \
    --exclude=tests . .

RUN adduser --no-create-home --disabled-password app \
    && chown -R app /app
USER app

ENTRYPOINT ["python", "main.py"]
