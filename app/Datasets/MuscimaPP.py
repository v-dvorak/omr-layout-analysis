from pathlib import Path
from omrdatasettools import Downloader, OmrDataset
from PIL import Image
import PIL.ImageOps

from .DatasetOMR import Dataset_OMR
from ..Utils import ParserUtils


class MuscimaPP(Dataset_OMR):
    """
    Dataset class of the Muscima++ dataset.
    """
    name = "Muscima++"
    nickname = "mpp"
    files_to_skip = ["all_measure_annotations.json",
                     "testing_measure_annotations.json",
                     "training_measure_annotations.json",
                     "validation_measure_annotations.json"]

    def _download_proc(self, download_path: Path):
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_MeasureAnnotations, download_path),
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_Images, download_path)

    def _get_coords(self, image_height: int, image_width: int, record: dict) -> list[float]:
        return ParserUtils.get_coords_relative_to_image_size(image_height, image_width,
                                                             record["left"],
                                                             record["top"],
                                                             abs(record["bottom"] - record["top"]),
                                                             abs(record["right"] - record["left"]))

    def _get_coco_format(self, record: dict) -> list[int]:
        return [record["left"],
                record["top"],
                abs(record["right"] - record["left"]),
                abs(record["bottom"] - record["top"])]

    def process_image(self, img_path: Path, output_path: Path):
        image = Image.open(img_path)
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(output_path)
