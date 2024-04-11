from .LabelKeeper import LabelKeeper
from .Label import Label
from ..Utils import LabelUtils
from ..Utils.Settings import Settings


class StaffSystem(LabelKeeper):
    """
    Represents a staff system - \"single line\" in musical notation that is related.
    Can be created from system measures.
    """
    def __init__(self, clss: int, system_measures: list[Label], offset: int = 10) -> None:
        self._system_measures: list[Label] = []     # 0
        self._stave_measures: list[Label] = []      # 1
        self._staves: list[Label] = []              # 2

        # variable init
        self._x: int
        self._y: int
        self._width: int
        self._height: int
        self._bottom: int
        self._right: int

        self._clss = clss

        self._offset = offset
        self._system_measures = system_measures
        self._complete_build()

    def _complete_build(self):
        """
        Internal method!

        Takes given labels and finds bounding box that encapsulates all of them.
        """
        self._x, self._y, self._width, self._height, self._right, self._bottom = LabelUtils.find_bbox_for_multiples_bboxes(
            self._system_measures)

    def is_in(self, label: Label) -> bool:
        """
        TODO:
        """
        return ((self._y - self._offset) < label.y < (self._bottom + self._offset))

    def get_coco_coordinates(self):
        """
        Returns coordinates encapsulating all given labels in COCO format, without! classification.
        """
        return [self._x, self._y, self._width, self._height]

    def get_coco_label(self):
        return [self._clss, *self.get_coco_coordinates()]

    def __str__(self) -> str:
        output = f"c: {Settings.NAME_SYSTEMS}, x: {self._x}, y: {self._y}, w: {self._width}, h: {self._height} \n"
        for label in self._staves:
            output += label.__str__() + "\n"
        return output

    def get_coco_to_dict(self):
        """
        Returns label in the COCO format without classification inside a dictionary

        Returns:
        - label in format ` {"left": x, "top": y, "width": width, "height": height}`
        """
        output = {}
        for lab, coord in zip(["left", "top", "width", "height"], self.get_coco_coordinates()):
            output[lab] = coord
        return output
