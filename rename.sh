#!/bin/bash

# Check if the required arguments are provided
if [ $# -ne 3 ]; then
    echo "Error: All SECRET_KEY and ACCESS_KEY REGION arguments are required."
    exit 1
fi

# Get the absolute path of the current working directory
WORKING_DIR=$(pwd | sed 's/\/terraform$//')

# Save the secret and access keys to variables
SECRET_KEY="$1"
ACCESS_KEY="$2"
REGION_KEY="$3"

# Escape special characters in the keys
ESCAPED_SECRET_KEY=$(printf '%s\n' "$SECRET_KEY" | sed -e 's/[]\/$*.^[]/\\&/g')
ESCAPED_ACCESS_KEY=$(printf '%s\n' "$ACCESS_KEY" | sed -e 's/[]\/$*.^[]/\\&/g')
ESCAPED_REGION_KEY=$(printf '%s\n' "$REGION_KEY" | sed -e 's/[]\/$*.^[]/\\&/g')


# Use sed to replace the values in the file
sed -i '' "s/^\( *\)\(export SECRET_KEY=.*\)/\\1export SECRET_KEY=\"$ESCAPED_SECRET_KEY\"/" "${WORKING_DIR}/ansible/master.yml"
sed -i '' "s/^\( *\)\(export ACCESS_KEY=.*\)/\\1export ACCESS_KEY=\"$ESCAPED_ACCESS_KEY\"/" "${WORKING_DIR}/ansible/master.yml"
sed -i '' "s/^\( *\)\(export REGION=.*\)/\\1export REGION=\"$ESCAPED_REGION_KEY\"/" "${WORKING_DIR}/ansible/master.yml"

