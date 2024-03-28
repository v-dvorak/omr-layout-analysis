from pathlib import Path
import shutil

from ..Parser import ParserUtils
from ..Parser import FileUtils

class Dataset_OMR:
    name = ""
    nickname = ""

    def _download_proc(self, download_path: Path):
        """
        Download procedure for getting the neccessary data using `OmrDataset` nad `Downloader` from `omrdatasettools`.
        
        Is dataset-specific.
        """
        raise NotImplementedError

    def download_dataset(self, where: Path, dataset_name: Path = None):
        """
        Downloads dataset using the `omrdatasettools` library. Stores it into given output file.        
        """
        if dataset_name is None:
            dataset_name = self.name
        download_path: Path = where / dataset_name #os.path.join(where, dataset_name)
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
    
    def process_image(self, img_path: Path, output_path: Path):
        shutil.copy(img_path, output_path)
    
    def process_label(self, label_path: Path, output_path: Path, labels: list[str], clean: bool = False):
        data = FileUtils.read_json(label_path)
        annot = self.parse_json_to_yolo(data, labels)
        if clean:
            annot = ParserUtils.get_unique_list(annot)
        FileUtils.write_rows_to_file(annot, output_path)
