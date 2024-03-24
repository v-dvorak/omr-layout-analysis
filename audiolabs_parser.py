#!/usr/bin/env python3

import shutil
import os
from tqdm import tqdm
import argparse
from parser_utils import *
from dataset_utils import *

# ARGUMENT SETUP
# TODO: description
parser = argparse.ArgumentParser(
    prog="OMR Dataset Parser",
    description="Parses data from given OMR datasets.",
    epilog=""
    )

# Required positional argument: output file name
parser.add_argument("output", help="Name and path to store the final dataset at.")

parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
parser.add_argument("-t", "--train", action="store_true", help="Create \"train\" subfolders")
parser.add_argument("-c", "--count", default=-1, help="How many files from each dataset will be processed. Default is all.")
parser.add_argument("--tag", action="store_true", help="Tags generated files with dataset nickname. Example: \"al2_filename\".")

parser.add_argument("-l","--labels", nargs="+", help="Which labels to process. 0 : system_measures, 1 : stave_measures, 2 : staves. Default is all.")
parser.add_argument("-s", "--dontsort", action="store_true", help="DONT sort labels by default numerical tags. Labels are sorted in ascending order by default.")


# DATASETS INIT
dataset_database = Dataset_OMR.__subclasses__() # Python magic
datasets_to_work_with = []

for current_dataset in dataset_database:
    parser.add_argument("--" + current_dataset.nickname,
                        action="store_true",
                        help=f"Includes the {current_dataset.name} dataset into final dataset.")

args = parser.parse_args()

# get dataset that will be processed
for current_dataset in dataset_database:
    if getattr(args, current_dataset.nickname):
        datasets_to_work_with.append(current_dataset)

if datasets_to_work_with == []:
    print("No datasets were specified, quitting job.")
    quit()

if args.verbose:
    print("Following datasets will be processed:")
    for dat in datasets_to_work_with:
        print(dat.name)

# LABELS INIT
POSSIBLE_LABELS = ["system_measures", "stave_measures", "staves"]
LABELS = []

if args.labels is None:
    LABELS = POSSIBLE_LABELS
else:
    args.labels = [int(x) for x in args.labels]
    if not args.dontsort:
        args.labels.sort()
    args.labels = make_list_unique(args.labels)
    for i in args.labels:
        LABELS.append(POSSIBLE_LABELS[i])


"""
AudioLabs structure:
{
    "width": 751,
    "height": 1057,
    "system_measures": [
        {
            "left": 77,
            "top": 232,
            "height": 102,
            "width": 111
        },
...

YOLO structure:
normalized!!
class x_center y_center width height
"""
# DIRECTORIES INIT
TRAIN_DATA_COUNT = int(args.count)
# set home for better navigation, everything is done in this working directory
HOME = os.path.abspath(os.path.join(args.output, ".."))
# create file structure to save data to
processed_dir = get_processed_number(HOME, args.output)
img_dir, labels_dir = create_file_structure(processed_dir, train=args.train)
create_yaml_file_for_yolo(processed_dir, img_dir, LABELS, args.verbose)

# MAIN LOOP
for dat_pos, current_dataset in enumerate(datasets_to_work_with):
    print()
    print(f"Processing {current_dataset.name}, {dat_pos+1}/{len(datasets_to_work_with)}")
    
    current_dataset.download_dataset(HOME)
    
    files_to_skip = current_dataset.files_to_skip
    tag = ""
    if args.tag: tag = current_dataset.nickname + "_"

    i = 0
    verbose = False
    img_processed = 0
    labels_processed = 0
    for subdir, dirs, files in tqdm(os.walk(os.path.join(HOME, current_dataset.name))):
        for file in files:
            if file in files_to_skip: continue

            if verbose: print(os.path.join(subdir, file))

            if file.endswith(".json") and (labels_processed < TRAIN_DATA_COUNT or args.count == -1):
                data = read_json(os.path.join(subdir, file))
                annot = current_dataset.parse_json_to_yolo(data, LABELS)
                write_rows_to_file(annot, os.path.join(labels_dir, tag + file.split(".")[0] + ".txt"))
                labels_processed += 1
                
            elif file.endswith(".png") and (img_processed < TRAIN_DATA_COUNT or args.count == -1):
                shutil.copy(os.path.join(subdir, file), os.path.join(img_dir, tag + file))
                img_processed += 1
            
            if not args.count == -1 and not labels_processed < TRAIN_DATA_COUNT and not img_processed < TRAIN_DATA_COUNT:
                break
        else:
            continue
        break

    print(f"Dataset {current_dataset.name} processed successfully, processed total of {img_processed} images.")

print("Job finished successfully, results are in:", os.path.abspath(processed_dir))