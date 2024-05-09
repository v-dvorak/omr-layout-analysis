#!/bin/bash

# Initialize variables
declare -a files=()
output_path=""
model_path="yolov8m.pt"
verbose=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output)
            output_path=$(realpath "$2")
            shift 2
            ;;
        -m|--model)
            model_path=$(realpath "$2")
            shift 2
            ;;
        -v|--verbose)
            verbose=true
            shift
            ;;
        *)
            files+=("$(realpath "$1")")
            shift
            ;;
    esac
done

# Check if files were specified
if [[ ${#files[@]} -eq 0 ]]; then
    echo "Error: No files specified."
    exit 1
fi

# Print parsed arguments
echo "Files to process:"
for file in "${files[@]}"; do
    echo "  $file"
done

# Construct the command to call the Python script
python_script_args=("${files[@]}" "-m" "$model_path")
if [[ -n "$output_path" ]]; then
    python_script_args+=("-o" "$output_path")
fi
if [[ "$verbose" == true ]]; then
    python_script_args+=("-v")
fi

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
python3 -m app.Predictions "${python_script_args[@]}"

# Revert to original directory
cd "$currentDirectory"
