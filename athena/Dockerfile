# syntax=docker/dockerfile:1

# This is the Dockerfile for the athena package.
# Its output is used as a dependency in the module_* Dockerfiles.

FROM python:3.11 as athena

WORKDIR /code

# Poetry
RUN pip install --no-cache-dir poetry==1.5.0

# Dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Project files
COPY . ./

# Build the package
RUN poetry build -f wheel
# The output is in /code/dist