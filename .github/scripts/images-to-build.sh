#!/bin/bash

# Get the commit hash of the branch creation
BASE_COMMIT=$(git merge-base develop $(git rev-parse --abbrev-ref HEAD))

# Get all changed files since branch creation
CHANGED_FILES=$(git diff --name-only $BASE_COMMIT)

# Initialize an empty array to hold directories
DIRS=()

# Loop over changed files
while IFS= read -r FILE; do
    # If a Dockerfile exists in the same directory as a changed file and the directory is in the root
    DIR=$(dirname "$FILE")
    if [[ -e "${DIR}/Dockerfile" && $DIR != *"/"* ]]; then
        # If not already in the array, add it
        if [[ ! " ${DIRS[@]} " =~ " ${DIR} " ]]; then
            DIRS+=("$DIR")
        fi
    fi
done <<< "$CHANGED_FILES"

# Print all directories that fulfill the conditions, separated by spaces
echo "${DIRS[@]}"
