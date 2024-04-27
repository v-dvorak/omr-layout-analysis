import argparse
from pathlib import Path

from .Oslic import OsLiC
from .AudioLabs import AudioLabs_v2
from .MuscimaPP import MuscimaPP
from .DatasetOMR import Dataset_OMR

# ARGUMENT SETUP
# TODO: description
parser = argparse.ArgumentParser(
    prog="Dataset downloader",
    description="Downloads all datasets specified by the user.",
    epilog=""
)

parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
# DATASETS ARGS INIT
# TODO: Add your newly defined dataset here
dataset_database = [
    AudioLabs_v2,
    MuscimaPP,
    OsLiC,
]

for i in range(len(dataset_database)):
    dataset_database[i] = dataset_database[i]()

# ADD OPTIONS TO ARGPARSE
# add arguments for datasets
for current_dataset in dataset_database:
    parser.add_argument("--" + current_dataset.nickname,
                        action="store_true",
                        help=f"Includes the {current_dataset.name} dataset into final dataset.")

args = parser.parse_args()

datasets_to_work_with: list[Dataset_OMR] = []
for current_dataset in dataset_database:
    if getattr(args, current_dataset.nickname):
        datasets_to_work_with.append(current_dataset)

for dat in datasets_to_work_with:
    dat.download_dataset(Path("datasets"))
