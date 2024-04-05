#!/usr/bin/env python3

import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

from ..Parser.FileStructure import FileStructure
from ..DatasetProcessor.DatasetProcessor import DatasetProcessor
from ..Datasets.Import import AudioLabs_v2
from ..DataMixer.DataMixer import DataMixer
import argparse

# ARGUMENT SETUP
# TODO: description
parser = argparse.ArgumentParser(
    prog="Grand Staff Annotator",
    # description="Compiles chosen OMR datasets into a big one for future use for training the YOLOv8 model.",
    epilog=""
    )

# Required positional argument: output file name
parser.add_argument("output", help="Path to store the final dataset at.")
parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
args = parser.parse_args()

# DIRECTORIES INIT
# set home for better navigation, everything is done in this working directory
HOME = Path.absolute(Path(args.output) / "..").resolve()

# create file structure to save data to
processed_dir = HOME
file_struct: FileStructure = FileStructure(HOME, "", "", "")

LABELS = ["system_measures", "stave_measures", "staves"]

# setup database, at this point in time only AudioLabs works
data_proc = DatasetProcessor([AudioLabs_v2()], LABELS, file_struct)
dat_mix: DataMixer = data_proc.load_dataset(AudioLabs_v2())
names = [dat.name for dat in dat_mix.get_all_data()]
names.sort()
numbers = []

class ImageViewer:
    def __init__(self, master, image_paths):
        self.master = master
        self.image_paths = image_paths
        self.current_index = 0

        self.label = tk.Label(master)
        self.label.pack()

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(master, textvariable=self.input_var)
        self.entry.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.process_and_next)
        self.submit_button.pack()

        # bind the Enter key to the process_and_next method - enter skips to next image
        self.master.bind("<Return>", lambda event: self.process_and_next())

        self.show_next_image()

    def show_next_image(self):
        if self.current_index < len(self.image_paths):
            image_path = self.image_paths[self.current_index]

            # load and display image
            image = Image.open(image_path)
            image.thumbnail((self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo
        else:
            # close window, all images were processed
            self.master.destroy()

    def process_and_next(self):
        data = self.input_var.get()
        process_data(self.image_paths[self.current_index], data)
        self.current_index += 1
        self.show_next_image()

def process_data(image_path, data):
    numbers.append(data)
    print(f"image: {image_path}")
    print("inputted data:", data)
    print()

def main():
    # window setup
    image_paths = [x.img_path for x in dat_mix.get_all_data()]
    root = tk.Tk()
    root.title("Piano Maker")

    image_viewer = ImageViewer(root, image_paths)  # noqa: F841

    root.mainloop()

    with open(Path(args.output), "w", encoding="utf8") as file:
        for i in range(len(numbers)):
            file.write(names[i])
            file.write("\n")
            file.write(numbers[i])
            file.write("\n")

    print(f"Output saved to {Path(args.output).absolute()}")

if __name__ == "__main__":
    main()