import numpy as np
import json
import yaml
from pathlib import Path

def make_list_unique(inp_list: list[any]) -> list[any]:
    """
    Takes a list and returns list of all the unique values
    that were inside given list in the original order.
    Ex: `[8,5,1,3,8,8,4,5,2]` becomes `[8,5,1,3,4,2]`.

    Args:
    - inp_list: input list
    
    Returns:
    - a list in which all values are unique
    """
    unique_list = []
    # got through all elements
    for x in inp_list:
        # check if item is already in list
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def get_coords_relative_to_image_size(image_height: int, image_width: int, left: int, top: int, height: int, width: int) -> list[float]:
    """
    Takes coordinates in "AudioLabs v2" notation and returns them in YOLO format.

    YOLO format:

    `class x_center y_center width height`, relative to image width and height
    """
    return np.round(
        [
            (left + width / 2) / image_width,
            (top + height / 2) / image_height,
            width / image_width,
            height / image_height,
        ],
        6,
    )

def read_json(filename: Path) -> dict:
    """
    Reads json file into a dict.

    Args:
    - filename: file to write to
    """
    with open(filename, "r", encoding="utf8") as file:
        # Load the file content into a JSON object
        return json.load(file)


def write_rows_to_file(data: list[list[int]], filename: Path, dato_sep="\t", record_sep="\n"):
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

def get_all_subdirs(working_dir: Path) -> list[Path]:
    return [x for x in working_dir.iterdir() if x.is_dir()]

def get_processed_number(working_dir: Path, folder_name: Path) -> Path:
    """
    Checks for files with same name inside given folder. Returns the new name of a file with a full path

    Example:
    If `name`, `name1`, `name2` are in directory, `name3` is returned.

    Args:
    - working_dir: directory in which the function will search in
    - folder_name: the `name` part of returned string
    """
    # clean up folder name string, mainly bcs of Windows shenanigans
    folder_name: str = folder_name.parts[-1]

    all_folders: list[Path] = get_all_subdirs(working_dir)
    # get ONLY folder names
    all_folder_names = [str(x.parts[-1]) for x in all_folders]
    # preprocess for transformation to ints
    all_folder_names = [x.replace(folder_name, "") for x in all_folder_names if x.startswith(folder_name)]
    if all_folder_names == []:
        latest = ""
    else:
        # clean up to ints
        clean: list[int] = []
        for x in all_folder_names:
            try:
                temp = int(x)
                clean.append(temp)
            except:  # noqa: E722
                pass
        
        clean.sort()
        if clean == []:
            latest = str(1)
        else:
            latest = str(clean[-1] + 1)

    return working_dir / (folder_name + latest)

def create_file_structure(processed_dir: Path, verbose: bool = False, train: bool = False) -> tuple[Path, Path]:
    """
    Creates folders for data.

    Args:
    - processed_dir: file in which all the processed dat will be stored
    - train: if true, train subfolder is added

    Returns:
    - locations to store images and labels to
    """
    img_dir = processed_dir / "images"
    labels_dir = processed_dir / "labels"
    if train:
        img_dir = img_dir / "train"
        labels_dir = labels_dir / "train"
    
    Path.mkdir(img_dir, parents=True)
    Path.mkdir(labels_dir, parents=True)

    return img_dir, labels_dir

def create_yaml_file_for_yolo(final_dataset_dir: Path, img_dir_train: Path, labels: list[str], img_dir_val: Path = None, file_name: str = "config", verbose: bool = False):
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
    if img_dir_val is None:
        img_dir_val = img_dir_train
    final_dataset_dir = str(final_dataset_dir.absolute().resolve())
    img_dir_train = str(img_dir_train.absolute().resolve())
    img_dir_val = str(img_dir_val.absolute().resolve())
    names = {}
    for i, label in enumerate(labels):
        names[i] = label

    data = {
        "path": final_dataset_dir,
        "train": img_dir_train,
        "val": img_dir_val,
        "names": names,
    }

    file_location = Path(final_dataset_dir + "/" + f"{file_name}.yaml")
    with open(file_location, "w") as file:
        yaml.dump(data, file, sort_keys=False)
    if verbose:
        print(f"{file_name}.yaml at {str(file_location.absolute())} created successfully.")