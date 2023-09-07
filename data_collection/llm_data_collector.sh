#!/bin/bash

# usage: ./auto_data_collector.sh <target_executable> <profile_period>
# example: ./auto_data_collector.sh ./tester/test 10

function init() {
    target_interpreter=$1
    target_executable=$2
    profile_period=$3
    events_list=()
    test_mode=0
    work_path=$(pwd)
    output_folder=$(basename ${target_executable})
    output_folder="${output_folder%.*}"
    output_path="$work_path/../output/$output_folder"
}

function user_check() {
    while true
    do
        read -r -p "Are these correct? [Y/n] " input
        case $input in
            [yY][eE][sS]|[yY])
                echo "Yes"
                break
                ;;
            [nN][oO]|[nN])
                echo "No"
                exit 1
                ;;
            *)
                echo "Invalid input..."
                ;;
        esac
    done
}

function executable_detection() {
    if [[ ! -f "$target_executable" ]]; then
        echo "$target_executable not found"
        exit 1
    fi
}

function path_detection() {
    if [[ ! -d "../output/ " ]]; then
        mkdir ../output
    fi

    if [[ ! -d "$output_path" ]]; then
        echo "$output_path not found"
        echo "creating......"
        mkdir $output_path
    fi
    echo "${output_path}"
}

function check_environment() {
    if [ $test_mode == 1 ]; then
        echo "Test mode enabled. No data will be collected."
    fi

    echo "Target executable: $target_executable"
    echo "The current working path is: "
    echo "${work_path}"
    echo "The path to the target executable is: "
    echo "${target_executable}"
    echo "The path to the Output Folder is: "
    path_detection $output_path
    user_check
}

function get_target_executable() {
    echo "Target executable: $target_executable"
}

function get_event_list() {
    input_file='events_list.txt'

    while IFS= read -r line; do
        events_list+=("$line")
    done < "$input_file"
}

function profile() {
    for element in "${events_list[@]}"; do
        echo "Collecting data for $element"
        perf stat -I 10 -e $element -o $output_path/$element.txt $target_interpreter $target_executable
    done
}

init $1 $2
executable_detection
# get_target_executable
check_environment
get_event_list
profile


