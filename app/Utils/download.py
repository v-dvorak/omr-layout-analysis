import os

from .BColors import print_done, print_header


def download():
    print_header("Downloading datasets:")
    os.system("python3 -m app.DatasetClasses --al2 --mpp --osl")
    print_done("Datasets downloaded.")

    print_header("Downloading negative samples:")
    os.system("python3 -m app.MZKBlank.download")
    print_done("Negative samples downloaded.")
