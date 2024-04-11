from .Label import Label
from .LabelKeeper import LabelKeeper
from .StaveSystem import StaffSystem
from ..Utils import ParserUtils, LabelUtils
from ..Utils.Settings import Settings

STAFF_SYSTEM_LABEL = 3
PIANO_LABEL = 4


class Sheet(LabelKeeper):
    """
    Represents a single sheet of paper.
    Can return bounding boxes of whole staff systems.
    """

    def __init__(self, annot: list[Label], labels: list[str], piano: list[list[int]] = None,
                 offset: int = 10, grand_limit: int = 0) -> None:
        self._system_measures: list[Label] = []         # 0
        self._stave_measures: list[Label] = []          # 1
        self._staves: list[Label] = []                  # 2

        self._staff_systems: list[StaffSystem] = []     # 3 !new in this class!
        self._grand_staff: list[Label] = []             # 4 !new in this class!
        
        self._grand_limit = grand_limit

        self._labels = labels

        self._offset = offset
        self._add_labels(annot)

        if Settings.NAME_SYSTEMS in labels:
            self.make_staff_system()
        
        if piano is not None:
            if Settings.NAME_GRAND_STAFF in labels:
                self.make_grand_staff(piano)

    def _get_all_labels(self) -> list[list[Label]]:
        return [self._system_measures, self._stave_measures, self._staves, self._staff_systems, self._grand_staff]

    def _sort_system_measures_into_systems(self):
        """
        Internal method!

        Sets up list of staff systems.
        """
        clss = self._labels.index(Settings.NAME_SYSTEMS)
        for labels in self._sort_into_bins(self._system_measures):
            self._staff_systems.append(StaffSystem(clss, labels))

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
        labels: list[Label] = sorted(labels, key=lambda elem: elem.y)
        bins: list[list[Label]] = [[]]

        for label in labels:
            added = False
            # check if label can be added to an existing bin
            for _bin in bins:
                if _bin != [] and abs(_bin[-1].y - label.y) <= self._offset:
                    _bin.append(label)
                    added = True
                    break
            # label couldn't be added to any existing bin, create a new bin
            if not added:
                bins.append([label])

        return bins[1::]

    def get_all_coco_labels(self) -> list[list[int]]:
        """
        Returns all labels in the COCO format with classification.

        Returns:
        - labels in format `[class, x, y, width, height]`
        """
        all_labels: list[list[Label]] = self._get_all_labels()
        output = []
        
        for labels in all_labels:
            for label in labels:
                output.append(label.get_coco_label())
        
        # if "systems" in self._labels:
        #     index = self._labels.index("systems")
        #     for label in self._staff_systems:
        #         output.append([index] + label.get_coco_coordinates())
        
        # for label in self._grand_staff:
        #     output.append(label.get_coco_label())

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

        # check
        described = sum([sum(x) for x in piano])
        if described < len(cur_s_s):
            print(f"WARNING ⚠️ : {described} staves are described but there are {len(cur_s_s)} staves in image.")
        if described > len(cur_s_s):
            print(f"ERROR ⚠️ : {described} staves are described but there are {len(cur_s_s)} staves in image.")
            print("Quitting job.")
            quit()

        i = 0
        for k in range(len(piano)):
            staff_collections = []
            for chunksize in piano[k]:
                if chunksize == 0 or chunksize < self._grand_limit:
                    break
                staff_collections.append(cur_s_s[i:i+chunksize])
                i += chunksize
            
            for labs in staff_collections:
                x, y, width, height, _, _ = LabelUtils.find_bbox_for_multiples_bboxes(labs)
                self._grand_staff.append(Label(index, x, y, width, height))

    def _get_all_loaded_labels(self):
        return [self._system_measures,
                self._stave_measures,
                self._staves,
                self._staff_systems,
                self._grand_staff]
    
    def _get_all_loaded_labels_with_names(self) -> tuple[list[list[Label]], list[str]]:
        return zip(self._get_all_loaded_labels(), Settings.LABELS)
    
    def _get_all_coco_to_dict(self):
        output = []
        for labels, name in self._get_all_loaded_labels_with_names():
            output.append((name, [label.get_coco_to_dict() for label in labels]))
        return output
    
    def get_coco_json_format(self, width: int, height: int) -> dict:
        output = {"width": width, "height": height}

        for name, coords in self._get_all_coco_to_dict():
            output[name] = coords

        return output
    
    def __str__(self) -> str:
        output = ""
        for labels, name in self._get_all_loaded_labels_with_names():
            output = output + "\n#" + name + "\n"
            for label in labels:
                output = output + label.__str__() + "\n"
        return output
