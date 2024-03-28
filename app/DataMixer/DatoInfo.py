from pathlib import Path

from ..Parser.FileUtils import get_file_name_from_path

class DatoInfo:
    """
    Holds information about one piece image from a dataset.
    """
    name: str = None
    img_path: Path = None
    label_path: Path = None

    def is_complete(self) -> bool:
        """
        Returns true if every part of neccessary data is set.
        To be considered "complete", object needs to know:

        - path to image file
        - path to file with labels
        - common name of these two files
        """
        return (
            self.name is not None
            and self.img_path is not None
            and self.label_path is not None
        )
    def __init__(self, img_path: Path):
        self.name = get_file_name_from_path(img_path)
        self.img_path = img_path