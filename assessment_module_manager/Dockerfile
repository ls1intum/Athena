# syntax=docker/dockerfile:1

# This is the Dockerfile for the assessment module manager.

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
    && poetry install --no-interaction --no-ansi # --without dev

# athena module (from the Dockerfile in the athena folder)
COPY --from=athena /code/dist /tmp/
RUN poetry add /tmp/athena-1.0.0-py3-none-any.whl

# Project files
COPY . ./

# Use modules configuration file for docker
RUN mv ./modules.docker.ini ./modules.ini

CMD poetry run assessment_module_manager