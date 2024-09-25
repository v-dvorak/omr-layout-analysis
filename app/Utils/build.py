import os
from datetime import datetime
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

    # add white backgrounds to transparent PNGs
    print_header("Adding white backgrounds to transparent PNGs:")
    os.system("python3 -m app.Synthetic.WhiteBackground")
    print_done("Background done.")

    # create annotations for Negative Samples dataset
    print_header("Creating annotations for negative samples:")
    os.system("python3 -m app.MZKBlank.build")
    print_done("Annotations created.")

    # collect all datasets and combine them into a single one
    print_header("Combining all datasets into one.")
    dataset_name = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_final_dataset"
    os.system(
        f"python3 -m app ./datasets/{dataset_name} --stad ./datasets/al2_gs ./datasets/mpp_gs ./datasets/Lieder-main ./datasets/MZKBlank")
    print_done(f"Datasets combined successfully, the final dataset is at {Path(dataset_name).resolve().absolute()}")
