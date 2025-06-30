FROM python:3.11.4-slim-bullseye AS prod


RUN pip install poetry==1.8.2

# Configuring poetry
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry_cache
# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies, including poppler-utils
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils libgl1 libglib2.0-0 tesseract-ocr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

# Copying actuall application
COPY . /app/src/
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

CMD ["/usr/local/bin/python", "-m", "rag"]

FROM prod AS dev

RUN --mount=type=cache,target=/tmp/poetry_cache poetry install
