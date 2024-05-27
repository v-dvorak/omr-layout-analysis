import argparse
from pathlib import Path

DATASET_DIR = Path("datasets/negative_samples/")
parser = argparse.ArgumentParser(
    prog="MZK negative sample downloader",
)

parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
parser.add_argument("-s", "--size",
                    default="^!640,640",
                    help="Image size that will be requested. Default is \"^!640,640\". For more "
                         "info see https://iiif.io/api/image/3.0/#42-size")

args = parser.parse_args()
