from pathlib import Path
import random

from .DatoInfo import DatoInfo
from ..Utils.FileUtils import get_file_name_from_path


class DataMixer:
    """
    Takes data from dataset files and converts them
    to a list of `DatoInfo` records that can be used later to process the dataset.
    """
    _data: list[DatoInfo] = []
    _cleaned: bool = False
    piano_annot: list[list[int]]

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

    def add_piano_annot(self, data: list[list[int]]):
        self.piano_annot = data
    
    def _clean_up(self):
        """
        Internal method!

        Iterates through all data in internal database and removes those
        that are not considered complete. This approach eliminates the need
        for a special list with files to ignore.
        """
        if not self._cleaned:
            self._data = [dato for dato in self._data if dato.is_complete()]
            self._cleaned = True
        
    def get_all_data(self) -> list[DatoInfo]:
        """
        Returns all data from the internal dataset. The dataset is cleaned before.
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

    @staticmethod
    def _check_ratio_in_bounds(ratio: float) -> bool:
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
            print(f"WARNING ⚠️ : Requested number of files ({whole_part}) is greater than the count of files in "
                  f"database ({len(self._data)}).\n{len(self._data)} files will be returned.")
        return True

    def train_test_split(self, ratio: float = 0.9, seed: int = None) -> tuple[list[DatoInfo], list[DatoInfo]]:
        """
        Splits the internal database by a given ration (default is 0.9) and returns them.
        The lengths of returned lists are: `total_length * ratio` and `total_length * (1 - ratio)`.

        Args:
        - ratio (optional) of two lengths of the two sets returned
        - seed (optional) seed for random number generator
        """
        self._check_ratio_in_bounds(ratio)
        self._clean_up()

        shuffled_data = self._data.copy()
        if seed is not None:
            random.Random(seed).shuffle(shuffled_data)
        else:
            random.shuffle(shuffled_data)

        split_index = round(len(self._data) * ratio)
        return shuffled_data[:split_index], shuffled_data[split_index:]
    
    def get_part_of_data(self, ratio: float = None, whole_part: int = None, seed: int = None) -> list[DatoInfo]:
        """
        Returns the requested part of the internal database.
        Length of list returned is `total_length * ratio` if ratio option is chosen,
        or `min(total_length, whole_part)` if whole part is chosen.
        Returns the first N elements of the internal database.
        """
        self._clean_up()

        shuffled_data = self._data.copy()
        if seed is not None:
            random.Random(seed).shuffle(shuffled_data)
        else:
            random.shuffle(shuffled_data)

        if ratio is not None:
            self._check_ratio_in_bounds(ratio)
            return shuffled_data[:round(len(self._data) * ratio)]
        elif whole_part is not None:
            self._check_whole_part_in_bounds(whole_part)
            return shuffled_data[:min(len(self._data), whole_part)]
