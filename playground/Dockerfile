# syntax=docker/dockerfile:1
FROM node:18.16.0-alpine

WORKDIR /app

# install packages
COPY package.json ./
COPY package-lock.json ./
RUN npm ci

# Copy the local code to the container's workspace
COPY . ./

# Set base path for deployment
ENV PLAYGROUND_BASE_PATH /playground

# Build the Next.js app
RUN npm run build

CMD [ "npm", "start" ]