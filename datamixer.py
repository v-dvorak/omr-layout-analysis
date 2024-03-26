from pathlib import Path
from random import shuffle
import numpy as np

def get_file_name_from_path(path: Path) -> str:
    return path.parts[-1].split(".")[0]

class DatoInfo:
    name: str = None
    img_path: Path = None
    label_path: Path = None

    def is_complete(self) -> bool:
        return (
            self.name is not None
            and self.img_path is not None
            and self.label_path is not None
        )
    def __init__(self, img_path: Path):
        self.name = get_file_name_from_path(img_path)
        self.img_path = img_path

class DataMixer:
    _data: list[DatoInfo] = []
    _cleaned: bool = False

    def __init__(self) -> None:
        self._data = []

    def add_image(self, img_path: Path):
        self._cleaned = False
        self._data.append(DatoInfo(img_path))
    
    def add_label(self, label_path: Path):
        self._cleaned = False
        label_name = get_file_name_from_path(label_path)
        for i in range(len(self._data)):
            if self._data[i].name == label_name:
                self._data[i].label_path = label_path

    def _clean_up(self):
        if not self._clean_up:
            self._data = [dato for dato in self._data if dato.is_complete()]
            self._cleaned = True
        
    def get_all_data(self):
        self._clean_up()
        return self._data
    
    def process_file_dump(self, img_paths: list[Path], label_paths: list[Path]):
        self._cleaned = False
        for img_path in img_paths:
            self.add_image(img_path)
        for label_path in label_paths:
            self.add_label(label_path)

    def count(self):
        return len(self._data)

    def _shuffle_data(self):
        shuffle(self._data)

    def _check_data_split(self, ratio: float):
        if ratio < 0 or ratio > 1:
            raise ValueError("Error: Split has to be a value between 0 and 1.")

    def train_test_split(self, ratio: float = 0.9) -> tuple[list[DatoInfo, DatoInfo]]:
        self._check_data_split(ratio)
        self._clean_up()
        return np.split(self._data, [round(len(self._data) * ratio)])
    # TODO: write a checker for ratio 0 < rat < 1 with custom error message
    def get_part_of_data(self, ratio: float = None, whole_part: int = None) -> list[DatoInfo]:
        self._clean_up()
        if ratio is not None:
            return self._data[:round(len(self._data) * ratio)]
        elif whole_part is not None:
            # TODO: think about letting eror of whole part slide or not
            if whole_part > len(self._data):
                print(f"WARNING ⚠️ : Requested number of files ({whole_part}) is greater than the count of files in database ({len(self._data)}).\n{len(self._data)} files will be returned.")
            return self._data[:min(len(self._data), whole_part)]