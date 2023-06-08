#!/bin/bash
target_executable=$1
work_path=$(pwd)
output_folder=$(basename ${target_executable})
output_folder="${output_folder%.*}"
echo ${output_folder}
output_path="$work_path/../$output_folder"
echo "${output_path}"


# path="/path/to/directory/filename.txt"

# # Extract the last filename
# filename=$(basename ${path})

# # Print the last filename
# echo "${filename}"