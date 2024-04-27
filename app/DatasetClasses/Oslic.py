import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

from .StandardCOCO import StandardCOCO


class OsLiC(StandardCOCO):
    """
    Dataset class of the AudioLabs v2 dataset.
    """
    name = "Lieder-main"
    nickname = "osl"

    def _download_proc(self, download_path: Path):
        ################################################
        # @author   Kristyna-Harvanova
        # @file     download_datasets.py
        # @at       https://github.com/Kristyna-Harvanova/Bachelor-Thesis/
        # @license  unspecified
        # used with minor tweaks
        ################################################
        download_dataset(
            "https://github.com/apacha/OMR-Datasets/releases/download/datasets/OpenScore-Lieder-Snapshot-2023-10-30.zip",
            "OpenScore-Lieder-Snapshot-2023-10-30.zip",
            download_path,
        )


def download_dataset(url: str, zip_file_name: str, dataset_dir: Path = Path("datasets")
):
    dataset_dir.mkdir(parents=True, exist_ok=True)

    file_path = dataset_dir / zip_file_name

    if file_path.exists():
        print("Dataset is already downloaded, quitting download job.")
        return

    response = requests.get(url, stream=True)

    with open(file_path, "wb") as file:
        for data in tqdm(response.iter_content()):
            file.write(data)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)
