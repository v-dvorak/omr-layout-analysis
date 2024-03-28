from pathlib import Path

class FileStructure:
    """
    Stores data about the dataset output file structure.
    """
    image: Path
    label: Path
    image_val: Path
    label_val: Path
    home: Path
    output: Path

    def __init__(self, home_dir: Path, output_dir: Path, image_dir: Path, label_dir: Path, image_val_dir: Path = None, label_val_dir: Path = None):
        self.home = home_dir
        self.output = output_dir
        self.image = image_dir
        self.label = label_dir
        self.image_val = image_val_dir
        self.label_val = label_val_dir

    def is_train_test(self):
        return (self.image_val is not None and self.label_val is not None)