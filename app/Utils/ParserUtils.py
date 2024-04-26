import numpy as np
from pathlib import Path


def coco_to_yolo(label: list[int], image_width: int, image_height: int):
    """
    Takes coordinates in COCO format with class number and returns coordinates in YOLO format.
    
    Args:
    - label: expected format `[class, left, top, width, height]`
    - image width
    - image height

    Returns:
    - coordinates in YOLO format with class, `[class, center x, center y, width, height]`
    , both width and height are relative to image size.
    """
    return [label[0]] + get_coords_relative_to_image_size(image_height, image_width, *label[1::])


def get_coords_relative_to_image_size(image_height: int, image_width: int,
                                      left: int, top: int, width: int, height: int) -> list[float]:
    """
    Takes coordinates in "AudioLabs v2" notation and returns them in YOLO format.

    YOLO format:

    `class x_center y_center width height`, relative to image width and height
    """
    return list(np.round(
        [
            (left + width / 2) / image_width,
            (top + height / 2) / image_height,
            width / image_width,
            height / image_height,
        ],
        6,
    ))


def get_unique_list(inp_list: list[any]) -> list[any]:
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


def print_parsing_error(file_path: Path, error: BaseException, i: int, total: int) -> None:
    print()
    print(f"⚠️ {i}/{total} Error when parsing: {file_path}")
    print(f"File name: {file_path.parts[-1]}")
    print(error)
    print()
