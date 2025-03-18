#!/bin/bash

image_dir="../images"
python_interpreter="${1:-/home/yao/anaconda3/envs/torch/bin/python}"


if [ ! -d "$image_dir" ]; then
    echo "Creating subdirectory: $image_dir"
    mkdir "$image_dir"
    if [ ! -f "test-annotations-bbox.csv" ]; then
        wget "https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv"  
    fi

    if [ ! -f "validation-annotations-bbox.csv" ]; then
        wget "https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv"
    fi

    if [ ! -f "oidv6-train-annotations-bbox.csv" ]; then
        wget "https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv"
    fi

    echo "Executing downloader.py with the interpreter: $python_interpreter"

    $python_interpreter "downloader.py" "image_list_file.txt" "--download_folder=$image_dir" "--num_processes=5"
    $python_interpreter "format_to_yolo.py"
else
    echo "Subdirectory already exists: $image_dir"
fi