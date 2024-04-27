from pathlib import Path
from omrdatasettools import Downloader, OmrDataset
from PIL import Image
import PIL.ImageOps

from .DatasetOMR import Dataset_OMR
from .download_dataset import download_dataset_from_url


class MuscimaPP(Dataset_OMR):
    """
    Dataset class of the Muscima++ dataset.
    """
    name = "Muscima++"
    nickname = "mpp"
    url = None
    zip_name = None

    def _download_proc(self, where: Path = Path("datasets")):
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_Images, where / self.name)
        Downloader().download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_MeasureAnnotations, where / self.name)

    def _get_coco_format(self, record: dict) -> list[int]:
        return [record["left"],
                record["top"],
                abs(record["right"] - record["left"]),
                abs(record["bottom"] - record["top"])]

    def process_image(self, img_path: Path, output_path: Path):
        image = Image.open(img_path)
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save(output_path)
