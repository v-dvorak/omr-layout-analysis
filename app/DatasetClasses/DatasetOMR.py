from pathlib import Path
import shutil
import json

from ..Utils import ParserUtils
from ..Utils.Settings import Settings
from ..Utils import FileUtils
from ..LabelKeeper.LabelKeeper import Label
from ..LabelKeeper.Sheet import Sheet
from .download_dataset import download_dataset_from_url


class Dataset_OMR:
    """
    \"Abstract\" base class from which all other dataset classes are derived.
    """
    name: str = None
    nickname: str = None
    download_url: str = None
    zip_name: str = None

    def __init__(self, maker_mode: bool = False):
        self.maker_mode = maker_mode
        pass

    def _get_coco_format(self, download_path: Path):
        """
        Download procedure for getting the necessary data using `OmrDataset` nad `Downloader` from `omrdatasettools`.
        
        Is dataset-specific.
        """
        raise NotImplementedError

    def download_dataset(self, where: Path = Path("datasets")):
        if (where / self.name).exists():
            print(f"Dataset {self.name} already downloaded")
            return
        else:
            self._download_proc(where)

    def _download_proc(self, where: Path = Path("datasets")):
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

        if self.maker_mode:
            for i, label in enumerate(labels[:3]):
                try:
                    for record in data[label]:
                        annot.append(Label(i, *self._get_coco_format(record)))
                except KeyError:
                    if label == Settings.NAME_GRAND_STAFF:
                        print(f"WARNING ⚠️ : Label \"{label}\" was not found in file description, skipping label.")
        else:
            for i, label in enumerate(labels):
                try:
                    for record in data[label]:
                        annot.append(Label(i, *self._get_coco_format(record)))
                except KeyError:
                    if label == Settings.NAME_GRAND_STAFF:
                        print(f"WARNING ⚠️ : Label \"{label}\" was not found in file description, skipping label.")

        return annot, (image_width, image_height)

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
        sheet = Sheet(annot, labels, piano=piano, offset=offset, grand_limit=grand_limit, maker_mode=True)
        temp = sheet.get_coco_json_format(image_size[0], image_size[1])
        with open(output_path, "w", encoding="utf8") as f:
            json.dump(temp, f, indent=True)

    def process_label(self, label_path: Path, output_path: Path, labels: list[str],
                      deduplicate: bool = False, maker_mode: bool = False):
        data = FileUtils.read_json(label_path)  # load data
        annot, image_size = self.parse_json_to_list(data, labels)  # get list of annotations and image size

        # label post-processing
        if deduplicate:
            annot = ParserUtils.get_unique_list(annot)

        # initialize sheet, get labels
        sheet = Sheet(annot, labels, maker_mode=maker_mode)
        annot = sheet.get_all_yolo_labels(image_size)

        # write
        FileUtils.write_rows_to_file(annot, output_path)
