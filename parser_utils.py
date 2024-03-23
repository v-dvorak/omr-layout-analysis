import numpy as np
import json
import os
import yaml
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

def download_dataset(zipurl: str, where: str, dataset_name: str) -> None:
    if os.path.exists(os.path.join(where, dataset_name)):
        print("Dataset has been already downloaded.")
        return
    else:
        os.makedirs(os.path.join(where, dataset_name))
        print(f"Downloading dataset from: {zipurl}")
        with urlopen(zipurl) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(os.path.join(where, dataset_name))
        print("Download finished successfully.")

def get_coords_relative_to_image_size(image_height: int, image_width: int, left: int, top: int, height: int, width: int) -> list[int]:
    """
    Takes coordinates in "AudioLabs v2" notation and returns them in YOLO format.
    """
    return np.round([(left + width / 2) / image_width, (top + height / 2) / image_height, width / image_width, height / image_height], 6)

def read_json(filename: str) -> dict:
    """
    Reads json file into a dict.

    Args:
    - filename: file to write to
    """
    with open(filename, 'r', encoding="utf8") as file:
        # Load the file content into a JSON object
        return json.load(file)

def write_rows_to_file(data: list[list[int]], filename: str, dato_sep="\t", record_sep="\n") -> None:
    """
    Write list of lists (list of annotation) to a specified file.

    Args:
    - data: data to write
    - filename: file to write to
    - dato_sep: separator between numbers in one record, default is `\\t`
    - record_sep: separator between records, default is `\\n`
    """
    with open(filename, "w", encoding="utf8") as file:
        for line in data:
            # class number is an int
            line[0] = str(line[0])
            # makes sure that every number has exactly six digits after decimal point
            # leads to better formatting
            for i in range(1, len(line)):
                line[i] = f"{line[i]:.6f}"
            file.write(dato_sep.join(line))
            file.write(record_sep)

def get_processed_number(working_dir: str, folder_name: str) -> str:
    """
    Checks for files with same name inside given folder. Returns the new name of a files.

    Example:
    If `name`, `name1`, `name2` are in directory, `name3` is returned.

    Args:
    - working_dir: directory in which the function will search in
    - folder_name: the `name` part of returned string
    """
    # clean up string, mainly bcs of Windows shenanigans
    folder_name = folder_name.replace("/", "")
    folder_name = folder_name.replace("\\", "")
    folder_name = folder_name.replace(".", "")
    
    all_folders = os.listdir(working_dir)
    all_folders = [lis for lis in all_folders if folder_name in lis]
    all_folders.sort()
    if all_folders == []:
        return folder_name
    else:
        latest = all_folders[-1].replace(folder_name, "")
        if latest != "":
            latest = str(int(latest) + 1)
        else:
            latest = "1"
        return folder_name + latest
    
def create_file_structure(processed_dir: str, verbose: bool = False, train: bool = False) -> tuple[str, str]:
    """
    Creates folders for data.

    Args:
    - processed_dir: file in which all the processed dat will be stored
    - train: if true, train subfolder is added

    Returns:
    - locations to store images and labels to
    """
    img_dir = os.path.join(processed_dir, "images")
    labels_dir = os.path.join(processed_dir, "labels")
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
        if verbose: print("Created file:", processed_dir)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        if verbose: print("Created file:", img_dir)
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
        if verbose: print("Created file:", labels_dir)

    if train:
        img_dir = os.path.join(img_dir, "train")
        labels_dir = os.path.join(labels_dir, "train")
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
            if verbose: print("Created file:", img_dir)
        if not os.path.exists(labels_dir):
            os.makedirs(labels_dir)
            if verbose: print("Created file:", labels_dir)
    return img_dir, labels_dir

def create_yaml_file_for_yolo(final_dataset_dir: str, img_dir_train: str, labels: list[str], img_dir_val: str = -1, verbose: bool = False) -> None:
    """
    Creates .yaml file in YOLO format neccessary for model training.

    Args:
    - final_dataset_dir: main directory where all the processed data is stored
    - img_dir_train: training images, image labels have to be at the same path except "images" in path is "labels"
    - labels: list of label names, is used to give labels numerical values for model training, ex:
        - `0: label0`
        - `1: label2`
        - ...
    """
    final_dataset_dir = os.path.abspath(final_dataset_dir)
    img_dir_train = os.path.abspath(img_dir_train)
    names = {}
    for i, label in enumerate(labels):
        names[i] = label
    
    data = {
        "path" : final_dataset_dir,
        "train" : img_dir_train,
        "val" : img_dir_train,
        "names" : names
    }

    with open(os.path.join(final_dataset_dir, "config.yaml"), 'w',) as file :
        yaml.dump(data, file, sort_keys=False) 
    if verbose: print('config.yaml at', os.path.abspath(os.path.join(final_dataset_dir, "config.yaml")), "created successfully.")