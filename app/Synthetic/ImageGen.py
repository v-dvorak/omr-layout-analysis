import os
import json
from pathlib import Path

from ..Utils.Settings import Settings

################################################
# @author   Kristyna-Harvanova
# @file     generate_images_for_oslic.py
# @at       https://github.com/Kristyna-Harvanova/Bachelor-Thesis/
# @license  unspecified
# used with minor tweaks
################################################


def convert_mscx2format(
        dataset_dir_path: Path,
        file_extension: str = "png"
):
    """ Convert all .mscx files in the dataset directory to the specified format. """

    # Create a JSON file for the conversion
    json_path = create_json_for_conversion(dataset_dir_path, file_extension)

    # Run the conversion
    os.system(
        f"{Settings.MUSESCORE_PATH} -j {json_path}")

    # Remove the JSON file
    os.remove(json_path)   #NOTE: netreba remove zatim asi, pokud ano, tak pouzit Path.unlink()???????


def create_json_for_conversion(
        dataset_dir_path: Path,
        file_extension: str = "png",
) -> Path:
    """ Create a JSON file for the conversion of all .mscx files in the dataset directory to the specified format. """
    conversion_list = []

    mscx_files = list(Path(dataset_dir_path).glob("**/*.mscx"))
    mscx_files.sort()  # Sort files if not in the same directory

    for in_path in mscx_files:
        # Construct the full paths for input and output files
        out_path = in_path.with_suffix(f".{file_extension}")

        # Add to conversion list
        conversion_list.append({
            "in": str(in_path),
            "out": str(out_path)
        })

    output_json_path = Path(dataset_dir_path, f"tmp_{file_extension}.json")

    with open(output_json_path, 'w') as json_file:
        json.dump(conversion_list, json_file, indent=4)

    return output_json_path
