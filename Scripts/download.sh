#!/bin/bash

# Store current working directory
currentDirectory=$(pwd)

# Get the directory of this script
module_directory=$(dirname "$(readlink -f "$0")")
module_directory=$(dirname "$module_directory")

# Change the working directory to the script directory temporarily
cd "$module_directory"

# Set the working directory to this script location
cd "$module_directory"

# Set the PYTHONPATH environment variable to include the module directory
export PYTHONPATH="$module_directory"

# Run the script
python3 -m app download

# Revert to original directory
cd "$currentDirectory"
