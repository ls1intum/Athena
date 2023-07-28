#!/bin/bash

# This script is used in the GitHub Actions workflow to determine which Docker images need to be built.
# We want to build a Docker image if at least one of the following conditions is true:
# 1. The Dockerfile in the directory has changed since the branch was created
# 2. The Docker image does not exist on GitHub Packages yet
# 3. The current branch is develop
# Otherwise, we want to skip the build for performance reasons.

# Stop on error
set -xe

# Fetch develop to find the commit hash of the branch creation
git fetch origin develop:develop

# Get the commit hash of the branch creation
BASE_COMMIT=$(git merge-base develop $(git rev-parse --abbrev-ref HEAD))

# Initialize an empty array to hold directories
DIRS=()

# Loop over all root level directories
for DIR in */; do
    # If a Dockerfile exists in the directory
    if [[ -e "${DIR}Dockerfile" ]]; then
        DIR=${DIR%/} # Remove trailing slash

        if [[ "$CURRENT_BRANCH" == "develop" ]]; then
            # Build all images on develop branch
            DIRS+=("$DIR")
            continue
        fi

        # Check if any file has changed in that directory since the branch was created
        GIT_DIFF=$(git diff --name-only $BASE_COMMIT -- "${DIR}")

        # Construct Docker image name and tag
        IMAGE_NAME="athena_${DIR}"
        IMAGE_TAG="pr-${GITHUB_PR_NUMBER}"

        # Check if Docker image exists on GitHub using API
        API_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/ls1intum/Athena/packages/container/${IMAGE_NAME}/versions?version=${IMAGE_TAG}")

        # If there are changes in the directory or the Docker image does not exist, add the directory to the array
        if [[ "$GIT_DIFF" != "" || "$API_RESPONSE" == "[]" ]]; then
            DIRS+=("$DIR")
        fi
    fi
done

# Print all directories that fulfill the conditions, separated by newlines
(IFS=$'\n'; echo "${DIRS[*]}")
