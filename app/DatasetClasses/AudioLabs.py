from pathlib import Path

from .DatasetOMR import Dataset_OMR
from .download_dataset import download_dataset_from_url


class AudioLabs_v2(Dataset_OMR):
    """
    Dataset class of the AudioLabs v2 dataset.
    """
    name = "AudioLabs_v2"
    nickname = "al2"
    download_url = "https://github.com/apacha/OMR-Datasets/releases/download/datasets/AudioLabs_v2.zip"
    zip_name = "AudioLabs_v2.zip"

    def _download_proc(self, where: Path = Path("datasets" )):
        download_dataset_from_url(
            self.download_url,
            self.zip_name,
            where / self.name
        )

    def _get_coco_format(self, record: dict) -> list[int]:
        output = []
        for key in ["left", "top", "width", "height"]:
            output.append(record[key])
        return output
