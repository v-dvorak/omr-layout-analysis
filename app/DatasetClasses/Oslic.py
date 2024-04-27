from pathlib import Path

from .StandardCOCO import StandardCOCO
from .download_dataset import download_dataset_from_url

class OsLiC(StandardCOCO):
    """
    Dataset class of the AudioLabs v2 dataset.
    """
    name = "Lieder-main"
    nickname = "osl"
    download_url = "https://github.com/apacha/OMR-Datasets/releases/download/datasets/OpenScore-Lieder-Snapshot-2023-10-30.zip"
    zip_name = "OpenScore-Lieder-Snapshot-2023-10-30.zip"

    def _download_proc(self, where: Path = Path("datasets")):
        download_dataset_from_url(
            self.download_url,
            self.zip_name,
            where
        )
