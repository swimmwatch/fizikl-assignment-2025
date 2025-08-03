ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION:-3.13}-slim as build

ARG POETRY_VERSION

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=${POETRY_VERSION}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc curl make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==${POETRY_VERSION}

# Set work directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy project
COPY . /app/
