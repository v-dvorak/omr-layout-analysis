from .Label import Label
from .LabelKeeper import LabelKeeper
from .StaveSystem import StaffSystem, find_bbox_for_multiples_bboxs
from ..Parser import ParserUtils

STAFF_SYSTEM_LABEL = 3
PIANO_LABEL = 4

class Sheet(LabelKeeper):
    """
    Represents a single sheet of paper.
    Can return bounding boxes of whoel staff systems.
    """

    def __init__(self, annot: list[Label], labels: list[str], piano: list[list[int]] = None, offset: int = 10) -> None:
        self._system_measures: list[Label] = []  # 0
        self._stave_measures: list[Label] = []   # 1
        self._staves: list[Label] = []           # 2

        self._staff_systems: list[StaffSystem] = [] # 3 !new in this class!
        self._grand_staff: list[Label] = [] # 4 !new in this class!
        
        self._labels = labels

        self._offset = offset
        self._add_labels(annot)

        if "system" in labels:
            self.make_staff_system()
        if "grand_staff" in labels:
            self.make_grand_staff(piano)
    
    def _sort_system_measures_into_systems(self):
        """
        Internal method!

        Sets up list of staff systems.
        """
        for labels in self._sort_into_bins(self._system_measures):
            self._staff_systems.append(StaffSystem(labels))

    def _sort_staves_to_systems(self):
        for staff in self._staves:
            self._add_label_to_system(staff)

    def _add_label_to_system(self, label: Label):
        for system in self._staff_systems:
            if system.is_in(label):
                system._add_label(label)
                break
    
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
        
        if "system" in self._labels:
            index = self._labels.index("system")
            for label in self._staff_systems:
                output.append([index] + label.get_coco_coordinates())
        
        for label in self._grand_staff:
            output.append(label.get_coco_label())

        return output
    
    def get_all_yolo_labels(self, image_size: tuple[int, int]) -> list[list[int]]:
        """
        Returns all labels in the YOLO format with classification.

        Args:
        - size: (width, height)

        Returns:
        - labels in format `[class, x center, y center, width, height]`, relative to image size
        """
        image_width, image_height = image_size
        output = []
        for label in self.get_all_coco_labels():
            output.append(ParserUtils.coco_to_yolo(label, image_width, image_height))
        return output
    
    def make_staff_system(self):
        self._sort_system_measures_into_systems()

    def make_grand_staff(self, piano: list[list[int]]):
        if self._staff_systems == []:
            self._sort_system_measures_into_systems()

        self._sort_staves_to_systems()
        cur_s_s = sorted(self._staves)
        index = self._labels.index("grand_staff")

        i = 0
        for k in range(len(piano)):
            pianinos = []
            for chunksize in piano[k]:
                if chunksize == 0:
                    break
                pianinos.append(cur_s_s[i:i+chunksize])
                i += chunksize
            
            for labs in pianinos:
                x, y, width, height, _, _ = find_bbox_for_multiples_bboxs(labs)
                self._grand_staff.append(Label(index, x, y, width, height))

    def __str__(self) -> str:
            all_labels = [self._system_measures, self._stave_measures, self._staves, self._staff_systems]
            output = ""
            names = ["system_measures", "stave_measures", "staves", "systems"]
            for i in range(len(all_labels)):
                output = output + "\n#" + names[i] + "\n"
                for label in all_labels[i]:
                    output = output + label.__str__() + "\n"
            return output