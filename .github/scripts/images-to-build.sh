#!/bin/bash

# This script is used in the GitHub Actions workflow to determine which Docker images need to be built.
# We want to build a Docker image if at least one of the following conditions is true:
# 1. The Dockerfile in the directory has changed since the branch was created
# 2. The Docker image does not exist on GitHub Packages yet
# 3. The current branch is develop
# Otherwise, we want to skip the build for performance reasons.

set -xe

# Initialize an empty array to hold directories
DIRS=()

# Get a list of all files changed in the current pull request
CHANGED_FILES=$(curl \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$GITHUB_REPO/pulls/$PR_NUMBER/files | jq -r '.[].filename')

# Loop over all root level directories
for DIR in */; do
    # If a Dockerfile exists in the directory
    if [[ -e "${DIR}Dockerfile" ]]; then
        DIR=${DIR%/} # Remove trailing slash

        # athena is always built and does not need to be re-built
        if [[ "$DIR" == "athena" ]]; then
            continue
        fi

        # no need to build docs
        if [[ "$DIR" == "docs" ]]; then
            continue
        fi

        if [[ "$GITHUB_REF" == "refs/heads/develop" ]]; then
            # Build all images on develop branch
            DIRS+=("$DIR")
            continue
        fi

        # Construct Docker image name and tag
        IMAGE_NAME="athena_${DIR}"
        IMAGE_TAG="pr-$PR_NUMBER"

        # Check if any file has changed in that directory since the pull request was created
        IS_CHANGED=$(echo "$CHANGED_FILES" | grep -q "^$DIR" && echo "true" || echo "false")
        # Check if Docker image exists on GitHub Packages
        URL="https://api.github.com/orgs/$ORGANIZATION_NAME/packages/container/$IMAGE_NAME"
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -L \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer ${GITLAB_TOKEN}" \
        https://api.github.com/orgs/$ORGANIZATION_NAME/packages/container/$IMAGE_NAME)
        # Check if the image exists
        if [ $RESPONSE -eq 200 ]; then
            IMAGE_EXISTS=true
        else
            IMAGE_EXISTS=false
        fi
        if [[ "$IS_CHANGED" == "true" || "$IMAGE_EXISTS" == "false" ]]; then
            # Add the directory to the array
            DIRS+=("$DIR")
        fi
    fi
done

# Print all directories that fulfill the conditions, separated by newlines
(IFS=$'\n'; echo "${DIRS[*]}")
