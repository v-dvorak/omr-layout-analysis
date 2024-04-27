################################################
# @author   Kristyna-Harvanova
# @file     download_datasets.py
# @at       https://github.com/Kristyna-Harvanova/Bachelor-Thesis/
# @license  unspecified
# used with minor tweaks
################################################

import requests
import zipfile
from pathlib import Path
from tqdm import tqdm


def download_dataset_from_url(url: str, zip_file_name: str, dataset_dir: Path = Path("datasets")):
    """
    Given a url downloads the zip file and saves it in given directory.
    """
    dataset_dir.mkdir(parents=True, exist_ok=True)

    file_path = dataset_dir / zip_file_name

    response = requests.get(url, stream=True)

    with open(file_path, "wb") as file:
        for data in tqdm(response.iter_content()):
            file.write(data)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)
