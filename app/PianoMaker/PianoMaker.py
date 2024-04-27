#!/usr/bin/env python3

from tqdm import tqdm
from pathlib import Path
from natsort import natsorted

from ..DatasetClasses.Import import Dataset_OMR
from ..DataMixer.DataMixer import DataMixer
from ..DataMixer.DatoInfo import DatoInfo
from ..Utils import FileUtils
from ..Utils.Settings import Settings


class PianoMaker:
    """
    Takes datasets to be processed, file structure and labels
    and optional arguments that determine the final form of the dataset.
    """
    # data control
    _LABELS: list[str] = Settings.LABELS

    def __init__(self,
                 dataset: Dataset_OMR,
                 dataset_path: Path,
                 output_path: Path,
                 piano_path: Path,
                 offset: int = 10,
                 grand_limit: int = 0,
                 verbose: bool = False,) -> None:
        
        self._DATASET: Dataset_OMR = dataset
        self._PIANO_ANNOT: list[list[int]] = None

        self.dataset_path: Path = dataset_path
        self.output_path: Path = output_path
        self.output_path_img: Path = None
        self.output_path_json: Path = None
        self.piano_path: Path = piano_path

        self._offset: int = offset
        self._grand_limit: int = grand_limit
        self._verbose: bool = verbose

    def print_dataset_names(self):
        """
        Prints out names of given datasets.
        """
        print("Following datasets will be processed:")
        print(self._DATASET.name)

    def _create_file_structure(self):
        # Create the base directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Create two subdirectories inside the base directory
        self.output_path_img = self.output_path / "img"
        self.output_path_json = self.output_path / "json"

        self.output_path_img.mkdir(exist_ok=True)
        self.output_path_json.mkdir(exist_ok=True)
    
    def process_dataset(self):
        self._create_file_structure()
        dat = self.load_dataset()
        self._PIANO_ANNOT = FileUtils.load_description_file_to_dictionary(self.piano_path)
        self._process_part_of_dataset(self._DATASET, dat.get_all_data(), self.output_path_img, self.output_path_json)
        
    def load_dataset(self) -> DataMixer:
        """
        Loads given dataset to a list of `DatoInfo`s.

        Args:
        - dataset to be loaded

        Returns:
        - `DataMixer` loaded with records from given dataset
        """
        dat = DataMixer()
        all_images_paths: list[Path] = natsorted((self.dataset_path.rglob("*.png")), key=Path)
        all_labels_paths: list[Path] = natsorted((self.dataset_path.rglob("*.json")), key=Path)
        dat.process_file_dump(all_images_paths, all_labels_paths)
        return dat

    def _process_part_of_dataset(self,
                                 current_dataset: Dataset_OMR,
                                 data: list[DatoInfo],
                                 image_path: Path,
                                 label_path: Path,
                                 tag: str = ""):
        """
        Base method for all other dataset file processing.
        Processes all files given in a `DataMixer` format.

        All used directories have to be setup BEFORE this method is called!

        Args:
        - dataset to be processed
        - `DataMixer` loaded with records from given dataset
        - path to save images to
        - path to save labels to
        - optional:
            - tags generated files at the beginning of their name with dataset nickname, e.g.: `\"al2_filename\"
        """

        for dato in tqdm(data):
            if self._verbose:
                print(dato.name)
                print(dato.img_path.parts[-1], dato.label_path.parts[-1])
            
            current_dataset.process_image(
                        dato.img_path,
                        image_path / (tag + dato.name + Settings.IMAGE_SAVE_FORMAT)
                    )
            current_dataset.preprocess_label(
                        dato.label_path,
                        label_path / (tag + dato.name + Settings.COCO_SAVE_FORMAT),
                        self._LABELS,
                        piano=self._PIANO_ANNOT[dato.name],
                        deduplicate=True,
                        grand_limit=self._grand_limit,
                        offset=self._offset
                    )
    
    def print_final_message(self):
        print(f"Job finished, results are at {self.output_path.absolute().resolve()}")
        print(f"Processed dataset: {self._DATASET.name}")
        print(f"With offset: {self._offset}")
        print(f"Minimal staves for grand staff: {self._grand_limit}")