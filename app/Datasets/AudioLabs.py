from pathlib import Path
from omrdatasettools import Downloader, OmrDataset

from .DatasetOMR import Dataset_OMR
from ..Utils import ParserUtils


class AudioLabs_v2(Dataset_OMR):
    """
    Dataset class of the AudioLabs v2 dataset.
    """
    name = "AudioLabs_v2"
    nickname = "al2"
    files_to_skip = ["all_annotations.json"]

    def _download_proc(self, download_path: Path):
        Downloader().download_and_extract_dataset(OmrDataset.AudioLabs_v2, download_path),

    def _get_coords(self, image_height: int, image_width: int, record: dict) -> list[float]:
        return ParserUtils.get_coords_relative_to_image_size(image_height, image_width,
                                                             record["left"],
                                                             record["top"],
                                                             record["height"],
                                                             record["width"])

    def _get_coco_format(self, record: dict) -> list[int]:
        output = []
        for key in ["left", "top", "width", "height"]:
            output.append(record[key])
        return output
