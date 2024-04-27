import os

from .BColors import print_done, print_header
from .download import download


def build():
    download()
    print_header("Preprocessing datasets, finding systems and grand staffs:")
    piano_dats = [
        ("Muscima++", "MPP_grand_staff.txt", "mpp_gs", "--mpp"),
        ("AudioLabs_v2", "AL2_grand_staff.txt", "al2_gs", "--al2"),
    ]
    for name, annot_path, out_path, specs in piano_dats:
        os.system(f"python3 -m app.PianoMaker ./datasets/{name} {annot_path} ./datasets/{out_path} {specs}")
        print_done(f"Preprocessing {name} done.")

    print_header("Preprocessing OSLiC dataset:")
    os.system(f"python3 -m app.Synthetic --png --svg")
    print_done("Preprocessing OSLiC done.")
