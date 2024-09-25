from pathlib import Path

from . import Utils

DATASET_DIR = Path("datasets/MZKBlank")
data = DATASET_DIR.rglob("*.png")
Utils.create_annotations(list(data), DATASET_DIR / "json")
