import os
from datetime import date
from pathlib import Path

from .BColors import print_done, print_header
from .download import download


def build():
    # download datasets
    download()

    # convert AL2 and MPP to COCO format, add systems and grand staffs
    print_header("Preprocessing datasets, analyzing systems and grand staffs:")
    piano_dats = [
        ("Muscima++", "MPP_grand_staff.txt", "mpp_gs", "--mpp"),
        ("AudioLabs_v2", "AL2_grand_staff.txt", "al2_gs", "--al2"),
    ]
    for name, annot_path, out_path, specs in piano_dats:
        os.system(f"python3 -m app.PianoMaker ./datasets/{name} {annot_path} ./datasets/{out_path} {specs}")
        print_done(f"Preprocessing {name} done.")

    # using MuseScore create PNGs adn SVGs for OSLiC, convert to COCO format
    print_header("Preprocessing OSLiC dataset:")
    os.system(f"python3 -m app.Synthetic --png --svg")
    print_done("Preprocessing OSLiC done.")

    # collect all datasets and combine them into a single one
    print_header("Combining all datasets into one.")
    dataset_name = f"{date.today().strftime('%Y_%m_%d')}_final_dataset"
    os.system(
        f"python3 -m app ./datasets/{dataset_name} --stad ./datasets/al2_gs ./datasets/mpp_gs ./datasets/Lieder-main")
    print_done(f"Datasets combined successfully, the final dataset is at {Path(dataset_name).resolve().absolut()}")