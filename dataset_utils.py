import os
from omrdatasettools import OmrDataset, Downloader
import parser_utils

class Dataset_OMR:
    name = ""
    nickname = ""

    def _download_proc(self, download_path: str) -> None:
        """
        Download procedure for getting the neccessary data using `OmrDataset` nad `Downloader` from `omrdatasettools`.
        
        Is dataset-specific.
        """
        raise NotImplementedError

    def download_dataset(self, where: str, dataset_name: str = -1) -> None:
        """
        Downloads dataset using the `omrdatasettools` library. Stores it into given output file.        
        """
        if dataset_name == -1:
            dataset_name = self.name
        download_path = os.path.join(where, dataset_name)
        if os.path.exists(download_path):
            return
        else:
            os.makedirs(download_path)
            self._download_proc(download_path)
    
    def _get_coords(self, image_height: int, image_width: int, record: dict) -> list[float]:
        """
        Takes image dimensions and data (parsed from JSON),
        returns coordinates in AudioLabs_v2 structure.
        These coordinates are ment to be transformed to YOLO's `xywh` format.
        
        Is dataset-specific.

        Args:
        - image_height:
        - image_width:
        - record: dictionary with information about one particular label, is dataset-specific

        Returns:
        - AL structure: `[left, top, height, width]` in absolute values.
        """
        raise NotImplementedError
    
    def parse_json_to_yolo(self, data: dict, labels: list[str]) -> list[list[int]]:
        """
        Takes data loaded from JSON into a dictionary and processes them into a list of records.
        Where each record corresponds to one labelled object.

        Args:
        - data: loaded JSON through the "json" library
        - labels: list of labels that are taken into account, labels not specified will not be processed

        Returns:
        - list of all found labels: in YOLO format, one label is one sublist
        """
        image_width, image_height = data["width"], data["height"]
        annot = []
        for i, label in enumerate(labels):
            for record in data[label]:
                annot.append([i, *self._get_coords(image_height, image_width, record)])
        return annot

class AudioLabs_v2(Dataset_OMR):
    name = "AudioLabs_v2"
    nickname = "al2"
    files_to_skip = ["all_annotations.json"]

    def _download_proc(self, download_path: str) -> None:
        Downloader().download_and_extract_dataset(OmrDataset.AudioLabs_v2, download_path),

    def _get_coords(self, image_height: int, image_width: int, record: dict) -> list[float]:
        return parser_utils.get_coords_relative_to_image_size(image_height, image_width,
                                                record["left"],
                                                record["top"],
                                                record["height"],
                                                record["width"])

class MuscimaPP(Dataset_OMR):
    name = "MusicmaPlusPlus"
    nickname = "mpp"
    files_to_skip = ["all_measure_annotations.json",
                     "testing_measure_annotations.json",
                     "training_measure_annotations.json",
                     "validation_measure_annotations.json"]

    def _download_proc(self, download_path: str) -> None:
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_MeasureAnnotations, download_path),
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_Images, download_path)

    def _get_coords(self, image_height: int, image_width: int, record: dict) -> list[float]:
        return parser_utils.get_coords_relative_to_image_size(image_height, image_width,
                                                record["left"],
                                                record["top"],
                                                abs(record["bottom"] - record["top"]),
                                                abs(record["right"] - record["left"]))