from .Label import Label
from .LabelKeeper import LabelKeeper
from .StaveSystem import StaffSystem
from ..Parser import ParserUtils

class Sheet(LabelKeeper):
    """
    Represents a single sheet of paper.
    Can return bounding boxes of whoel staff systems.
    """

    def __init__(self, labels: list[Label], offset: int = 10) -> None:
        self._system_measures: list[Label] = []  # 0
        self._stave_measures: list[Label] = []   # 1
        self._staves: list[Label] = []           # 2

        self._staff_system: list[StaffSystem] = [] # 3 !new in this class!
        
        self._offset = offset
        self._add_labels(labels)
        self._split_into_systems()
    
    def _split_into_systems(self):
        """
        Internal method!

        Sets up list of staff systems.
        """
        for labels in self._sort_into_bins(self._system_measures):
            self._staff_system.append(StaffSystem(labels))
    
    def _sort_into_bins(self, labels: list[Label]) -> list[list[Label]]:
        """
        Sorts given list of labels using a greedy algorithm.
        To be sorted into a bin, label needs to be offset-close to the last label in the bin.

        Args:
        - labels: list of labels, can be different classes or mixed classes

        Returns:
        - list of bins
        """
        labels: list[Label] = sorted(labels, key=lambda label: label.y)
        bins: list[list[Label]] = [[]]

        for label in labels:
            added = False
            # check if label can be added to an existing bin
            for bin in bins:
                if bin != [] and abs(bin[-1].y - label.y) <= self._offset:
                    bin.append(label)
                    added = True
                    break
            # label coouldnt be added to any existing bin, create a new bin
            if not added:
                bins.append([label])

        return bins[1::]

    def get_all_coco_labels(self) -> list[list[int]]:
        """
        Returns all labels in the COCO format with classification.

        Returns:
        - labels in format `[class, x, y, width, height]`
        """
        all_labels: list[list[Label]] = [self._system_measures, self._stave_measures, self._staves]
        output = []
        
        for labels in all_labels:
            for label in labels:
                output.append(label.get_coco_label())
        
        STAFF_SYSTEM_LABEL = 3
        for label in self._staff_system:
            output.append([STAFF_SYSTEM_LABEL] + label.get_coco_coordinates())
        
        return output
    
    def get_all_yolo_labels(self, image_width: int, image_height: int) -> list[list[int]]:
        """
        Returns all labels in the YOLO format with classification.

        Args:
        - image width
        - image height

        Returns:
        - labels in format `[class, x center, y center, width, height]`, relative to image size
        """
        output = []
        for label in self.get_all_coco_labels():
            output.append(ParserUtils.coco_to_yolo(label, image_width, image_height))
        return output
    
    def __str__(self) -> str:
        all_labels = [self._system_measures, self._stave_measures, self._staves, self._staff_system]
        output = ""
        names = ["system_measures", "stave_measures", "staves", "systems"]
        for i in range(len(all_labels)):
            output = output + "\n#" + names[i] + "\n"
            for label in all_labels[i]:
                output = output + label.__str__() + "\n"
        return output