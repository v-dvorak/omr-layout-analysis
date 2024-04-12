#!/usr/bin/env python3

import argparse
from pathlib import Path

from ..Datasets.Import import Dataset_OMR, AudioLabs_v2, MuscimaPP, StandardCOCO
from .PianoMaker import PianoMaker

# ARGUMENT SETUP
# TODO: description
parser = argparse.ArgumentParser(
    prog="OMR Dataset Utils",
    description="Given a dataset and a file with additional labels makes a JSON combining both current dataset labels and the new ones.",
    epilog=""
    )

# Required positional argument: output file name
parser.add_argument("dataset_path", help="Path to dataset to be processed.")
parser.add_argument("piano_path", help="Path to grand staff annotations.")
parser.add_argument("output_path", help="Path to store the final dataset at.")

parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose.")
parser.add_argument("-o", "--offset", default=10, help="How far apart two coordinates can be to still be considered the same, in pixels. Default is 10.")
parser.add_argument("-l", "--grand_limit", default=1, help="Minimal amount of staves to consider multiple staves linked together to be a grand staff. Default is 1.")


# DATASETS INIT
dataset_database = Dataset_OMR.__subclasses__() # Python magic
for i in range(len(dataset_database)):
    if dataset_database[i].__name__ == "StandardCOCO":
        del dataset_database[i]
    else:
        dataset_database[i] = dataset_database[i](maker_mode=True)

# ADD OPTIONS TO ARGPARSE
# add arguments for datasets
for current_dataset in dataset_database:
    parser.add_argument("--" + current_dataset.nickname,
                        action="store_true",
                        help=f"The {current_dataset.name} dataset will be processed.")

args = parser.parse_args()

# get dataset that will be processed
datasets_to_work_with: list[Dataset_OMR] = []
for current_dataset in dataset_database:
    if getattr(args, current_dataset.nickname):
        datasets_to_work_with.append(current_dataset)

if datasets_to_work_with == []:
    print("No datasets were specified, quitting job.")
    quit()
if len(datasets_to_work_with) > 1:
    print("Too many datasets were specified, specify only one at a time, quitting job.")
    quit()

pm = PianoMaker(datasets_to_work_with[0], Path(args.dataset_path), Path(args.output_path), Path(args.piano_path),
                offset=int(args.offset), grand_limit=int(args.grand_limit), verbose=args.verbose)

pm.process_dataset()
pm.print_final_message()