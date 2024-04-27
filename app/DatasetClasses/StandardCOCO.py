from pathlib import Path

from .DatasetOMR import Dataset_OMR
from ..Utils import ParserUtils


class StandardCOCO(Dataset_OMR):
    """
    Dataset class of the AudioLabs v2 dataset.
    """
    name = "Standard Dataset"
    nickname = "stand"

    def _download_proc(self, download_path: Path):
        raise NotImplementedError("Standard dataset cannot be downloaded")

    def _get_coco_format(self, record: dict) -> list[int]:
        output = []
        for key in ["left", "top", "width", "height"]:
            output.append(record[key])
        return output
