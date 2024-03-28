from pathlib import Path
from random import shuffle
import numpy as np

from .DatoInfo import DatoInfo
from ..Parser.FileUtils import get_file_name_from_path

class DataMixer:
    _data: list[DatoInfo] = []
    _cleaned: bool = False

    def __init__(self) -> None:
        self._data = []

    def add_image(self, img_path: Path):
        """
        Adds given image (path to the image) to the internal database.

        Args:
        - path to image
        """
        self._cleaned = False
        self._data.append(DatoInfo(img_path))
    
    def add_label(self, label_path: Path):
        """
        Adds given label (path to file with labels) to the internal database.

        Args:
        - path to file with labels
        """
        self._cleaned = False
        label_name = get_file_name_from_path(label_path)
        for i in range(len(self._data)):
            if self._data[i].name == label_name:
                self._data[i].label_path = label_path

    def _clean_up(self):
        """
        Internal method!

        Iterates throught all data in internal database and removes those
        that are not considered complete. This approach eliminates the need
        for a special list with files to ignore.
        """
        if not self._cleaned:
            self._data = [dato for dato in self._data if dato.is_complete()]
            self._cleaned = True
        
    def get_all_data(self) -> list[DatoInfo]:
        """
        Retuns all data from the internal dataset. The dataset is cleaned before.
        """
        self._clean_up()
        return self._data
    
    def process_file_dump(self, img_paths: list[Path], label_paths: list[Path]):
        """
        Processes lists of files and adds them to internal database.

        Args:
        - list of paths to images
        - list of paths to files with labels
        """
        self._cleaned = False
        for img_path in img_paths:
            self.add_image(img_path)
        for label_path in label_paths:
            self.add_label(label_path)

    def count(self) -> int:
        """
        Returns the current length of the internal database.
        """
        return len(self._data)

    def _shuffle_data(self):
        """
        Shuffles data in the internal database randomly.
        Based on `shuffle` from the `random` library.
        """
        shuffle(self._data)

    def _check_ratio_in_bounds(self, ratio: float) -> bool:
        """
        Internal method!

        Checks if ratio is in bounds,
        raises ValueError if not.
        """
        if ratio < 0 or ratio > 1:
            raise ValueError("Error: Split has to be a value between 0 and 1.")
        return True
    
    def _check_whole_part_in_bounds(self, whole_part: int):
        if whole_part > len(self._data):
            print(f"WARNING ⚠️ : Requested number of files ({whole_part}) is greater than the count of files in database ({len(self._data)}).\n{len(self._data)} files will be returned.")
        return True

    def train_test_split(self, ratio: float = 0.9) -> tuple[list[DatoInfo], list[DatoInfo]]:
        """
        Splits the internal database by a given ration (default is 0.9) and returns them.
        The lengths of retuned lists are: `total_length * ratio` and `total_length * (1 - ratio)`.

        Args:
        - ratio (optional) of two leghts of the two sets returned
        """
        self._check_ratio_in_bounds(ratio)
        self._clean_up()
        return np.split(self._data, [round(len(self._data) * ratio)])
    
    def get_part_of_data(self, ratio: float = None, whole_part: int = None) -> list[DatoInfo]:
        """
        Returns the requested part of the internal database.
        Length of list retuned is `total_length * ratio` if ratio option is chosen,
        or `min(total_length, whole_part)` if whole part is chosen.
        Returns the first N elements of the internal database.
        """
        self._clean_up()
        if ratio is not None:
            self._check_ratio_in_bounds(ratio)
            return self._data[:round(len(self._data) * ratio)]
        elif whole_part is not None:
            self._check_whole_part_in_bounds(whole_part)
            return self._data[:min(len(self._data), whole_part)]