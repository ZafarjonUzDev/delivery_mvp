FROM python:3.12.16-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && groupadd --system django \
    && useradd --system --gid django --no-create-home django

COPY --chown=django:django . .
USER django

EXPOSE 8000

# Local development server. Migrations are a separate, explicit command.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
