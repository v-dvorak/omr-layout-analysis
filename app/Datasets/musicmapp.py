from pathlib import Path
from omrdatasettools import Downloader, OmrDataset

from .DatasetOMR import Dataset_OMR
from ..Parser import FileUtils

class MuscimaPP(Dataset_OMR):
    name = "MusicmaPlusPlus"
    nickname = "mpp"
    files_to_skip = ["all_measure_annotations.json",
                     "testing_measure_annotations.json",
                     "training_measure_annotations.json",
                     "validation_measure_annotations.json"]

    def _download_proc(self, download_path: Path):
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_MeasureAnnotations, download_path),
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_Images, download_path)

    def _get_coords(self, image_height: int, image_width: int, record: dict) -> list[float]:
        return FileUtils.get_coords_relative_to_image_size(image_height, image_width,
                                                record["left"],
                                                record["top"],
                                                abs(record["bottom"] - record["top"]),
                                                abs(record["right"] - record["left"]))