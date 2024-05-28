from pathlib import Path
from PIL import Image
import json
from tqdm import tqdm

from ..Utils.Settings import Settings


def create_annotations(img_paths: list[Path], output_dir: Path, verbose=False):
    output_dir.mkdir(exist_ok=True, parents=True)

    for img_path in tqdm(img_paths):
        image = Image.open(img_path)
        width, height = image.size
        annot = EMPTY_ANNOT
        annot["width"] = width
        annot["height"] = height
        with open(output_dir / (img_path.stem + ".json"), "w", encoding="utf8") as f:
            json.dump(annot, f, indent=4)


EMPTY_ANNOT = {
    "width": 0,
    "height": 0,
    Settings.NAME_SYSTEM_MEASURE: [],
    Settings.NAME_STAVE_MEASURE: [],
    Settings.NAME_STAVES: [],
    Settings.NAME_SYSTEMS: [],
    Settings.NAME_GRAND_STAFF: []
}
