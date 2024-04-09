#!/usr/bin/env python3

from tqdm import tqdm
from pathlib import Path
from natsort import natsorted

from ..Parser import FileUtils
from ..Datasets.Import import Dataset_OMR
from ..DataMixer.DataMixer import DataMixer
from ..Parser.FileStructure import FileStructure
from ..DataMixer.DatoInfo import DatoInfo

class DatasetProcessor:
    """
    Takes datasets to be processed, file structure and labels
    and optional arguments that determine the final form of the dataset.
    """
    # data control
    _DATASETS: list[Dataset_OMR]
    _LABELS: list[str]
    _file_struct: FileStructure
    # volume control
    _split: float
    _count: int

    _tag: bool
    _deduplicate: bool
    _verbose: bool

    def __init__(self,
                 datasets: list[Dataset_OMR],
                 labels: list[str],
                 file_struct: FileStructure,
                 verbose: bool = False,
                 split: float = None,
                 count: int = None,
                 deduplicate: bool = False,
                 tag: bool = False) -> None:
        
        self._DATASETS = datasets
        self._LABELS = labels
        self._file_struct = file_struct
        self._split = split
        self._count = count
        self._tag = tag
        self._deduplicate = deduplicate
        self._verbose = verbose

        self._run_checks()

    def print_datataset_names(self):
        """
        Prints out names of given datasets.
        """
        print("Following datasets will be processed:")
        for dat in self._DATASETS:
            print(dat.name)

    def _run_checks(self):
        """
        Internal method!

        Runs necessary checks after initilization.
        """
        if self._split is not None:
            self._check_ratio_in_bounds()
        self._check_split_ratio_def()
    
    def _check_ratio_in_bounds(self) -> bool:
        """
        Internal method!

        Checks if ratio is in bounds,
        raises ValueError if not.
        """
        if self._split < 0 or self._split > 1:
            raise ValueError("Error: Split has to be a value between 0 and 1.")
        return True
    
    def _check_split_ratio_def(self):
            """
            Internal method!

            Checks if dataset is big enough to fulfill users demands.
            Raises a warning if not.
            """
            if self._count is not None and self._split is not None:
                print(f"WARNING ⚠️ : Split is set to {float(self._split)}, Count will have no effect on output.")

    def create_yaml_file(self):
        """
        Creates .yaml file in YOLO format neccessary for model training.
        """
        FileUtils.create_yaml_file_for_yolo(self._file_struct, self._LABELS)
        
    def load_dataset(self, current_dataset: Dataset_OMR) -> DataMixer:
        """
        Loads given dataset to a list of `DatoInfo`s.

        Args:
        - dataset to be loaded

        Returns:
        - `DataMixer` loaded with records from given dataset
        """
        dat = DataMixer()
        all_images_paths: list[Path] = natsorted(((self._file_struct.home / current_dataset.name).rglob("*.png")), key=str)
        all_labels_paths: list[Path] = natsorted(((self._file_struct.home / current_dataset.name).rglob("*.json")), key=str)
        dat.process_file_dump(all_images_paths, all_labels_paths)
        return dat
    
    def process_all_datasets(self):
        """
        Iterates through all datasets given at initialization and processes them.
        """
        for dataset in self._DATASETS:
            self.process_dataset(dataset)
        
        print("Job finished successfully, results are in:", Path(self._file_struct.output).absolute().resolve())

    def process_dataset(self, current_dataset: Dataset_OMR):
        """
        Processes single given dataset.

        Args:
        - dataset to be processed
        """
        data_mixer = self.load_dataset(current_dataset)

        tag = ""
        if self._tag:
            tag = current_dataset.nickname + "_"
        
        if self._split is not None:
            self.split_process_dataset(current_dataset, data_mixer, tag)
        else:
            self.count_process_dataset(current_dataset, data_mixer, tag)
        
        print(f"Dataset {current_dataset.name} processed successfully.")

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
                
        # piano_annot = FileUtils.load_description_file_to_dictionary("ALv2_grand_staff.txt")

        for dato in tqdm(data):
            if self._verbose:
                # print(piano_annot[dato.name])
                print(dato.name)
                print(dato.img_path.parts[-1], dato.label_path.parts[-1])
            
            current_dataset.process_image(
                        dato.img_path,
                        image_path / (tag + dato.name + ".png")
                    )
            current_dataset.process_label(
                        dato.label_path,
                        label_path / (tag + dato.name + ".txt"),
                        self._LABELS,
                        # piano=piano_annot[dato.name],
                        clean=self._deduplicate
                    )

    def count_process_dataset(self, current_dataset: Dataset_OMR, data_mixer: DataMixer, tag: str = ""):
        """
        Processes single given dataset, takes only first `count` of records.
        `count` is given at initialization.

        All used directories have to be setup BEFORE this method is called!

        Args:
        - dataset to be processed
        - `DataMixer` loaded with records from given dataset
        - optional:
            - tags generated files at the beginning of their name with dataset nickname, e.g.: `\"al2_filename\"`
        """
        if self._count is None:
            to_process = data_mixer.get_all_data()
        else:
            to_process = data_mixer.get_part_of_data(whole_part=self._count)
        
        self._process_part_of_dataset(current_dataset, to_process,
                                      self._file_struct.image, self._file_struct.label,
                                      tag)            

    def split_process_dataset(self, current_dataset: Dataset_OMR, data_mixer: DataMixer, tag: str = ""):
        """
        Processes single given dataset, splits records into train and test file by the `split` ratio.
        `split` is given at initialization.

        All used directories have to be setup BEFORE this method is called!

        Args:
        - dataset to be processed
        - `DataMixer` loaded with records from given dataset
        - optional:
            - tags generated files at the beginning of their name with dataset nickname, e.g.: `\"al2_filename\"`
        """
        data = data_mixer.train_test_split(ratio=self._split)
        # TRAIN
        self._process_part_of_dataset(current_dataset, data[0],
                                      self._file_struct.image, self._file_struct.label,
                                      tag)
        # TEST
        self._process_part_of_dataset(current_dataset, data[1],
                                      self._file_struct.image_val, self._file_struct.label_val,
                                      tag)