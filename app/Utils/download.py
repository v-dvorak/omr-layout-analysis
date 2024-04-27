import os

from .BColors import print_done, print_header


def download():
    print_header("Downloading datasets:")
    os.system("python3 -m app.DatasetClasses --mpp --al2 --osl")
    print_done("DatasetClasses downloaded.")
