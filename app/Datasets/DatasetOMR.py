from pathlib import Path
import shutil
import json

from ..Utils import ParserUtils
from ..Utils import FileUtils
from ..LabelKeeper.LabelKeeper import Label
from ..LabelKeeper.Sheet import Sheet


class Dataset_OMR:
    """
    \"Abstract\" base class from which all other dataset classes are derived.
    """
    name = ""
    nickname = ""

    def __init__(self, maker_mode: bool = False) -> None:
        self._maker_mode = maker_mode
        pass

    def _download_proc(self, download_path: Path):
        """
        Download procedure for getting the necessary data using `OmrDataset` nad `Downloader` from `omrdatasettools`.
        
        Is dataset-specific.
        """
        raise NotImplementedError

    def _get_coco_format(self, download_path: Path):
        """
        Download procedure for getting the necessary data using `OmrDataset` nad `Downloader` from `omrdatasettools`.
        
        Is dataset-specific.
        """
        raise NotImplementedError

    def download_dataset(self, where: Path, dataset_name: Path = None):
        """
        Downloads dataset using the `omrdatasettools` library. Stores it into given output file.        
        """
        if dataset_name is None:
            dataset_name = self.name
        download_path: Path = where / dataset_name
        if download_path.exists():
            return
        else:
            Path.mkdir(download_path)
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

    def parse_json_to_list(self, data: dict, labels: list[str]) -> tuple[list[Label], tuple[int, int]]:
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

        if self._maker_mode:
            for i, label in enumerate(labels[:3]):
                try:
                    for record in data[label]:
                        annot.append(Label(i, *self._get_coco_format(record)))
                except KeyError:
                    if label == "grand_staff":
                        print(f"WARNING ⚠️ : Label \"{label}\" was not found in file description, skipping label.")
        else:
            for i, label in enumerate(labels):
                try:
                    for record in data[label]:
                        annot.append(Label(i, *self._get_coco_format(record)))
                except KeyError:
                    if label == "grand_staff":
                        print(f"WARNING ⚠️ : Label \"{label}\" was not found in file description, skipping label.")

        return annot, (image_width, image_height)

    def _legacy_parse_json_page(self, data: dict, labels: list[str]) -> list[list[Label]]:
        # TODO: think about removal
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
        # TODO: FIX this AAAAAAAAAA, this is now a legacy code. remove it
        for i, label in enumerate(labels[:3]):
            # for i, label in enumerate(labels):
            for record in data[label]:
                annot.append([i, *self._get_coords(image_height, image_width, record)])
        return annot

    def process_image(self, img_path: Path, output_path: Path):
        shutil.copy(img_path, output_path)

    def preprocess_label(self, label_path: Path, output_path: Path, labels: list[str], piano: list[int] = None,
                         deduplicate: bool = False,
                         offset: int = 10, grand_limit: int = 0):
        data = FileUtils.read_json(label_path)  # load data
        annot, image_size = self.parse_json_to_list(data, labels)  # get list of annotations and image size
        # label post-processing
        if deduplicate:
            annot = ParserUtils.get_unique_list(annot)

        # initialize sheet, get labels
        sheet = Sheet(annot, labels, piano=piano, offset=offset, grand_limit=grand_limit)
        temp = sheet.get_coco_json_format(image_size[0], image_size[1])
        with open(output_path, "w", encoding="utf8") as f:
            json.dump(temp, f, indent=True)

    def process_label(self, label_path: Path, output_path: Path, labels: list[str], deduplicate: bool = False):
        data = FileUtils.read_json(label_path)  # load data
        annot, image_size = self.parse_json_to_list(data, labels)  # get list of annotations and image size

        # label post-processing
        if deduplicate:
            annot = ParserUtils.get_unique_list(annot)

        # initialize sheet, get labels
        sheet = Sheet(annot, labels)
        annot = sheet.get_all_yolo_labels(image_size)

        # write
        FileUtils.write_rows_to_file(annot, output_path)
