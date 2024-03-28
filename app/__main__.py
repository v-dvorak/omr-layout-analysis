#!/usr/bin/env python3

from .Parser import parser_utils
from .Datasets.dataset_import import Dataset_OMR
from .DataMixer.datamixer import DataMixer
from tqdm import tqdm
import argparse
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
parser.add_argument("-c", "--count", default=None, help="How many files from each dataset will be processed. Default is all.")
parser.add_argument("--tag", action="store_true", help="Tags generated files with dataset nickname. Example: \"al2_filename\".")
parser.add_argument("-l","--labels", nargs="+", help="Which labels to process. 0 : system_measures, 1 : stave_measures, 2 : staves. Default is all.")
parser.add_argument("--split", default=None, help="Train test split ratio.")
parser.add_argument("--clean", action="store_true", help="Checks for possible duplicates in labels and remove them. May affect performance.")

# DATASETS INIT
dataset_database = Dataset_OMR.__subclasses__() # Python magic
for i in range(len(dataset_database)):
    dataset_database[i] = dataset_database[i]()

# ADD OPTION TO ARGPARSE
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
    args.labels = parser_utils.get_unique_list(args.labels)
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
processed_dir = parser_utils.get_processed_number(HOME, Path(args.output))
img_dir, labels_dir = parser_utils.create_file_structure(Path(processed_dir), train=(args.split is not None))

# YAML CONFIG
if args.split is None:
    parser_utils.create_yaml_file_for_yolo(processed_dir, img_dir, LABELS, verbose=args.verbose)
else:
    parser_utils.create_yaml_file_for_yolo(processed_dir, img_dir[0], LABELS, img_dir_val=img_dir[1], verbose=args.verbose)

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
    
    dat = DataMixer()
    dat.process_file_dump(all_images_paths, all_labels_paths)
    dat._shuffle_data()

    # EVERYTHING TOGEHTER
    if args.split is None:
        if args.count is None:
            to_process = dat.get_all_data()
        else:
            to_process = dat.get_part_of_data(whole_part=args.count)
        
        for dato in tqdm(to_process):
            if args.verbose:
                print(dato.img_path.parts[-1], dato.label_path.parts[-1])
            
            current_dataset.process_image(
                        dato.img_path,
                        img_dir / (tag + dato.name + ".png")
                    )
            current_dataset.process_label(
                        dato.label_path,
                        labels_dir / (tag + dato.name + ".txt"),
                        LABELS,
                        clean=args.clean
                    )
    # SEPARATE TRAIN AND VAL FILES
    else:
        for i in [0, 1]: # train data, val data (aka test data)
            if args.verbose:
                print("train:" if i == 0 else "val:")
            for dato in tqdm(dat.train_test_split(ratio=args.split)[i]):
                if args.verbose:
                    print(dato.img_path.parts[-1], dato.label_path.parts[-1])
                
                current_dataset.process_image(
                            dato.img_path,
                            img_dir[i] / (tag + dato.name + ".png")
                        )
                current_dataset.process_label(
                            dato.label_path,
                            labels_dir[i] / (tag + dato.name + ".txt"),
                            LABELS,
                            clean=args.clean
                        )

    print(f"Dataset {current_dataset.name} processed successfully.")

print("Job finished successfully, results are in:", Path(processed_dir).absolute().resolve())