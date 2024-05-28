from . import ImageUtils
import json
from pathlib import Path

DATASET_DIR = Path("datasets/NegativeSamples")

with open("app/NegativeSamples/scraped_data/chosen.json", "r", encoding="utf8") as f:
    data = json.load(f)

dimensions = {
    "blank": (20, 27),
    "front_cover": (5, 9),
    "front_end_sheet": (5, 9),
    "back_end_sheet": (5, 8),
    "back_cover": (5, 8),
    "title_page": (14, 15),
    "back_end_paper": (4, 5),
    "table_of_contents": (1, 7),
    "index": (3, 4),
    "front_end_paper": (4, 5),
    "illustration": (1, 1),
    "fragments_of_bookbinding": (1, 1)
}

for key in data.keys():
    if key == "count":
        continue

    images = list(DATASET_DIR.rglob(f"{key}_*.png"))
    ImageUtils.combine_images_into_grid(images, *dimensions[key], size=(200, 200),
                                        output_path=f"app/NegativeSamples/docs/{key}_grid.png")
