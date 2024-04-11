#!/usr/bin/env python3

import argparse
from pathlib import Path

from .Utils import ParserUtils, FileUtils
from .Utils.FileStructure import FileStructure
from .Datasets.Import import Dataset_OMR, AudioLabs_v2, MuscimaPP
from .DatasetProcessor.DatasetProcessor import DatasetProcessor

# ARGUMENT SETUP
# TODO: description
parser = argparse.ArgumentParser(
    prog="OMR Dataset Utils",
    description="Compiles chosen OMR datasets into a big one for future use for training the YOLOv8 model.",
    epilog=""
    )

# Required positional argument: output file name
parser.add_argument("output", help="Path to store the final dataset at.")

parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
parser.add_argument("-c", "--count", default=None, help="How many files from each dataset will be processed. Default is all.")
parser.add_argument("--tag", action="store_true", help="Tags generated files with dataset nickname. Example: \"al2_filename\".")
parser.add_argument("-l", "--labels", nargs="+", help="Which labels to process. 0 : system_measures, 1 : stave_measures, 2 : staves. Default is all.")
parser.add_argument("--stad", nargs="+", help="Paths to standard COCO dataset.")
parser.add_argument("--split", default=None, help="Train test split ratio.")
parser.add_argument("--deduplicate", action="store_true", help="Checks for possible duplicates in labels and removes them. May affect performance.")

# DATASETS ARGS INIT
# dataset_database = Dataset_OMR.__subclasses__() # Python magic
dataset_database = [AudioLabs_v2, MuscimaPP]
for i in range(len(dataset_database)):
    dataset_database[i] = dataset_database[i]()


# ADD OPTIONS TO ARGPARSE
# add arguments for datasets
for current_dataset in dataset_database:
    parser.add_argument("--" + current_dataset.nickname,
                        action="store_true",
                        help=f"Includes the {current_dataset.name} dataset into final dataset.")

args = parser.parse_args()

# DATASETS TO PROCESS
# predefined
datasets_to_work_with: list[Dataset_OMR] = []
for current_dataset in dataset_database:
    if getattr(args, current_dataset.nickname):
        datasets_to_work_with.append(current_dataset)

# standard, given by path
if args.stad is not None:
    standard_datasets_to_work_with = [Path(x) for x in args.stad]
else:
    standard_datasets_to_work_with = []

dat_count = len(standard_datasets_to_work_with + datasets_to_work_with)

if dat_count == 0:
    print("No datasets were specified, quitting job.")
    quit()

if args.verbose:
    print("Following datasets will be processed:")
    for dat in datasets_to_work_with:
        print(dat.name)

# LABELS INIT
POSSIBLE_LABELS = ["system_measures", "stave_measures", "staves", "systems", "grand_staff"]
LABELS: list[str] = []

if args.labels is None:
    LABELS = POSSIBLE_LABELS
else:
    args.labels = [int(x) for x in args.labels]
    args.labels = ParserUtils.get_unique_list(args.labels)
    args.labels.sort()
    for i in args.labels:
        LABELS.append(POSSIBLE_LABELS[i])

# DATA SPLIT INIT
if args.split is not None:
    args.split = float(args.split)

if args.count is not None:
    args.count = int(args.count)
    if args.split is not None:
        print(f"WARNING ⚠️ : Split is set to {args.split}, Count will have no effect on output.")

# DIRECTORIES INIT
# set home for better navigation, everything is done in this working directory
HOME = Path.absolute(Path(args.output) / "..").resolve()

# create file structure to save data to
processed_dir = FileUtils.get_processed_number(HOME, Path(args.output))
file_struct: FileStructure = FileUtils.create_file_structure(Path(processed_dir), HOME, train=(args.split is not None))
if args.verbose:
    file_struct.print()

# YAML CONFIG
FileUtils.create_yaml_file_for_yolo(file_struct, LABELS)

# DATASET DOWNLOAD
for current_dataset in datasets_to_work_with:
    current_dataset.download_dataset(file_struct.home)

# DATASET PROCESSING
dp = DatasetProcessor(LABELS, file_struct,
                      split=args.split, count=args.count, deduplicate=args.deduplicate, tag=args.tag,
                      verbose=args.verbose)
for dataset in datasets_to_work_with:
    dp.process_dataset_from_fls(dataset)
for dataset_path in standard_datasets_to_work_with:
    dp.process_dataset_from_path(dataset_path)

print("Job finished successfully, results are in:", Path(file_struct.output).absolute().resolve())
# dp.process_all_datasets(datasets_to_work_with)