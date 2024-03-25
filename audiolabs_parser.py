#!/usr/bin/env python3

from tqdm import tqdm
import argparse
import parser_utils
from dataset_utils import Dataset_OMR
from pathlib import Path
from natsort import natsorted

# ARGUMENT SETUP
# TODO: description
parser = argparse.ArgumentParser(
    prog="OMR Dataset Parser",
    description="Compiles chosen OMR datasets into a big one for future use for training the YOLOv8 model.",
    epilog=""
    )

# Required positional argument: output file name
parser.add_argument("output", help="Path to store the final dataset at.")

parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
parser.add_argument("-t", "--train", action="store_true", help="Create \"train\" subfolders")
parser.add_argument("-c", "--count", default=None, help="How many files from each dataset will be processed. Default is all.")
parser.add_argument("--tag", action="store_true", help="Tags generated files with dataset nickname. Example: \"al2_filename\".")

parser.add_argument("-l","--labels", nargs="+", help="Which labels to process. 0 : system_measures, 1 : stave_measures, 2 : staves. Default is all.")
parser.add_argument("-s", "--dontsort", action="store_true", help="DONT sort labels by default numerical tags. Labels are sorted in ascending order by default.")


# DATASETS INIT
dataset_database = Dataset_OMR.__subclasses__() # Python magic
for i in range(len(dataset_database)):
    dataset_database[i] = dataset_database[i]()

# add arguments for datasets
for current_dataset in dataset_database:
    parser.add_argument("--" + current_dataset.nickname,
                        action="store_true",
                        help=f"Includes the {current_dataset.name} dataset into final dataset.")

args = parser.parse_args()

# get dataset that will be processed
datasets_to_work_with: list[Dataset_OMR] = []
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
LABELS: list[str] = []

if args.labels is None:
    LABELS = POSSIBLE_LABELS
else:
    args.labels = [int(x) for x in args.labels]
    if not args.dontsort:
        args.labels.sort()
    args.labels = parser_utils.make_list_unique(args.labels)
    for i in args.labels:
        LABELS.append(POSSIBLE_LABELS[i])

# DIRECTORIES INIT
TRAIN_DATA_COUNT = int(args.count)
# set home for better navigation, everything is done in this working directory
HOME = Path.absolute(Path(args.output) / "..")
print(HOME)
# create file structure to save data to
processed_dir = parser_utils.get_processed_number(HOME, args.output)
img_dir, labels_dir = parser_utils.create_file_structure(processed_dir, train=args.train)
parser_utils.create_yaml_file_for_yolo(processed_dir, img_dir, LABELS, verbose=args.verbose)

# MAIN LOOP
for dat_pos, current_dataset in enumerate(datasets_to_work_with):
    print()
    print(f"Processing {current_dataset.name}, {dat_pos+1}/{len(datasets_to_work_with)}")
    
    current_dataset.download_dataset(HOME)
    
    files_to_skip = current_dataset.files_to_skip
    tag = ""
    if args.tag:
        tag = current_dataset.nickname + "_"

    i = 0
    all_images_paths: list[Path] = natsorted(((HOME / current_dataset.name).rglob("*.png")), key=str)
    all_labels_paths: list[Path] = natsorted(((HOME / current_dataset.name).rglob("*.json")), key=str)

    for i in tqdm(range(TRAIN_DATA_COUNT)):
        file_name = all_images_paths[i].parts[-1]
        current_dataset.process_image(
                    all_images_paths[i],
                    Path(img_dir + "/" + tag + file_name)
                )
        current_dataset.process_label(
                    all_labels_paths[i],
                    Path(labels_dir + "/" + tag + file_name.split(".")[0] + ".txt"),
                    LABELS
                )

    print(f"Dataset {current_dataset.name} processed successfully, processed total of {TRAIN_DATA_COUNT} images.")

print("Job finished successfully, results are in:", Path(processed_dir).absolute())