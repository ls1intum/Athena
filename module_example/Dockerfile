# syntax=docker/dockerfile:1

# This is the Dockerfile for the module_example.

FROM python:3.11
LABEL org.opencontainers.image.source=https://github.com/pal03377/Athena-New

# Environment variable Python in Docker
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Poetry
RUN pip install --no-cache-dir poetry==1.5.0

# Dependencies
COPY pyproject.toml poetry.lock ./
# install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# athena module (from the Dockerfile in the athena folder)
COPY --from=athena /code /athena
RUN poetry add /athena

# Project files
COPY . ./

CMD poetry run module