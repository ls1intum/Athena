# syntax=docker/dockerfile:1
FROM node:18.16.0-alpine

LABEL org.opencontainers.image.source=https://github.com/ls1intum/Athena

WORKDIR /app

ARG ATHENA_BRANCH
ENV NEXT_PUBLIC_ATHENA_BRANCH $ATHENA_BRANCH
ARG ATHENA_PR_NUMBER
ENV NEXT_PUBLIC_ATHENA_PR_NUMBER $ATHENA_PR_NUMBER
ARG ATHENA_COMMIT_SHA
ENV NEXT_PUBLIC_ATHENA_COMMIT_SHA $ATHENA_COMMIT_SHA

# install packages
COPY package.json ./
COPY package-lock.json ./
RUN npm ci

# Copy the local code to the container's workspace
COPY . ./

# Build the Next.js app
RUN npm run build

CMD [ "npm", "start" ]