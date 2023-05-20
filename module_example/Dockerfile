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
# athena module (from the Dockerfile in the athena folder)
COPY --from=athena /code/dist ./
# install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev --with docker


# Project files
COPY . ./

CMD poetry run python -m module_example