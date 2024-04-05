from pathlib import Path
import json
import yaml
from .FileStructure import FileStructure
from typing import Dict

def load_description_file_to_dictionary(file_path) -> Dict[str, list[list[int]]]:
    """
    Loads given file into dictionary. 
    File has to be in a specific format:
    ```
    key
    value
    key
    value
    ...
    ```
    Where key is a name of file (not path to the file, only its name without extension)
    and value is a sequence of numbers describing staves and systems in the picture.
    """

    """
    Annotation formatting:
    - numbers correspong to number of staves in a grand staff
    - numbers connected by `-` are part of the same system
    Example:
    - `1-2 2-2 2` - there is a total of three systems in this file
        - first: one staff and a grand staff made up of two staves
        - second: two grand staffs made up of two staves
        - third: one grand staff made up of two staves    
    """
    data_dict = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # iterate over lines in pairs (name and data)
        for i in range(0, len(lines), 2):
            name = lines[i].strip()
            data = lines[i + 1].strip()
            data_dict[name] = [[int(a) for a in x.split("-")] for x in data.split(" ")]
    return data_dict

def get_file_name_from_path(path: Path) -> str:
    """
    Takes the last part of the path considered to be a file name
    and trims of its file extension.

    `folder/subfolder/example.txt -> example`

    Args:
    - path to file

    Returns:
    - name of file as a string
    """
    return path.parts[-1].split(".")[0]

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

def create_file_structure(processed_dir: Path, home_dir: Path, verbose: bool = False,
                          train: bool = False) -> FileStructure:
    """
    Creates folders for data.

    Args:
    - processed_dir: file in which all the processed dat will be stored
    - train: if true, train subfolder is added

    Returns:
    - locations to store images and labels to
    """
    img_dir = processed_dir / "images"
    label_dir = processed_dir / "labels"
    if train:
        img_dir_train = img_dir / "train"
        label_dir_train = label_dir / "train"
        img_dir_val = img_dir / "val"
        label_dir_val = label_dir / "val"
        for path in [img_dir_train, label_dir_train, img_dir_val, label_dir_val]:
            Path.mkdir(path, parents=True)
        # return (img_dir_train, img_dir_val), (labels_dir_train, labels_dir_val)
        return FileStructure(home_dir, processed_dir,
                             img_dir_train, label_dir_train,
                             img_dir_val, label_dir_val)
    else:
        Path.mkdir(img_dir, parents=True)
        Path.mkdir(label_dir, parents=True)

    return FileStructure(home_dir, processed_dir,
                         img_dir,
                         label_dir)

def create_yaml_file_for_yolo(file_struct: FileStructure, labels: list[str], file_name: str = "config", verbose: bool = False):
    """
    Creates .yaml file in YOLO format neccessary for model training.

    Args:
    - file_struct: list of directories import for the project
    - labels: list of label names, is used to give labels numerical values for model training, ex:
        - `0: label0`
        - `1: label2`
        - ...
    - optional:
        - file_name: final file name is `file_name.yaml`, default is "config"
        - verbose
    """
    if file_struct.is_train_test():
        img_dir_val = file_struct.image_val
    else:
        img_dir_val = file_struct.image
    
    final_dataset_dir = str(file_struct.output.absolute().resolve())
    img_dir_train = str(file_struct.image.absolute().resolve())
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

###############
# LEGACY CODE #
###############

def _legacy_create_yaml_file_for_yolo(final_dataset_dir: Path, img_dir_train: Path, labels: list[str], img_dir_val: Path = None, file_name: str = "config", verbose: bool = False):
    """
    Creates .yaml file in YOLO format neccessary for model training.

    Args:
    - final_dataset_dir: main directory where all the processed data is stored
    - img_dir_train: training images, image labels have to be at the same path except "images" in path is "labels"
    - labels: list of label names, is used to give labels numerical values for model training, ex:
        - `0: label0`
        - `1: label2`
        - ...
    - optional:
        - img_dir_val: if data are separated into train and test data, this is the list of the test data
        - file_name: final file name is `file_name.yaml`, default is "config"
        - verbose
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