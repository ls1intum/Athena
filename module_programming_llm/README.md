# Module Programming LLM

This system implements an approach for (semi-)automated assessment of programming exercises.

It implements the approach described in the following master's thesis:
> **An LLM-Enabled Approach for Automated Feedback Generation on Programming Exercises**  
> Felix T.J. Dietrich

## Setup


1. Fill in the following environment variables in the `.env` file of the module:

```
OPENAI_API_KEY= # openai api key (!)
PROMPTLAYER_API_KEY= # promptlayer api key (optional)
```

2. Install dependencies with poetry:

```
poetry install
```

## Usage

### Start Directly

`poetry run module`

### Start with Docker

`docker-compose up --build`

### Start with Docker in Production Mode

`docker-compose up --env-file .env.production --build`