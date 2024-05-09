from ultralytics import YOLO
from glob import glob
import argparse
import json
from pathlib import Path

from ..Utils.BColors import print_done, print_header
from .PredUtils import process_predicted_values

# TODO: description
parser = argparse.ArgumentParser(
    prog="TODO",
    description="TODO",
    epilog=""
)

# Required positional argument: output file name
parser.add_argument("files", nargs="+", help="Files to process")

parser.add_argument("-o", "--output", default=None, help="Path to store the final dataset at.")
parser.add_argument("-m", "--model", default="yolov8m.pt", help="Path to trained model.")
parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")

args = parser.parse_args()

# load model
model = YOLO(args.model)

# expand files
files_to_process = []
for file in args.files:
    files_to_process += glob(file)

print_header(f"Processing {len(files_to_process)} files...")

output = {}
i = 0
total = len(files_to_process)
for result in model.predict(files_to_process, verbose=args.verbose):
    if args.verbose:
        print(f"{i}/{total}", end='\r')
    output[Path(files_to_process[i]).resolve().__str__()] = process_predicted_values(result)
    i += 1

print_done("Done processing files.")
if args.output is not None:
    print_header(f"Saving results.")
    with open(Path(args.output.strip()), "w") as f:
        json.dump(output, f, indent=4)
    print_done(f"Results saved at {Path(args.output.strip()).resolve().absolute()}.")
else:
    print(json.dumps(output, indent=4))
