from .LabelKeeper import LabelKeeper
from .Label import Label

def find_bbox_for_multiples_bboxs(labels: list[Label]):
    """
    Given a bunch of rectangles we need to find the "most-left", "most-up", etc.
    points.
    
    +→ x
    ↓
    y
        3
        |
    1---+-------+---2
                |
                4
    """
    # 1
    x = min(labels, key=lambda label: label.x).x
    # 2
    max_right_measure =  max(labels, key=lambda label: label.x)
    right = max_right_measure.x + max_right_measure.width

    # 3
    y = min(labels, key=lambda label: label.y).y
    # 4
    max_down_measure = max(labels, key=lambda label: label.y)
    bottom = max_down_measure.y + max_down_measure.height

    # | 2 - 1 |
    width = right - x
    # | 4 - 3 |
    height = bottom - y

    return (x, y, width, height, right, bottom)

class StaffSystem(LabelKeeper):
    """
    Represents a staff system - \"single line\" in musical notation that is related.
    Can me created from system measures.
    """
    
    def __init__(self, system_measures: list[Label], offset: int = 10) -> None:
        self._system_measures: list[Label] = []  # 0
        self._stave_measures: list[Label] = []   # 1
        self._staves: list[Label] = []           # 2

        # variable init
        self._x: int
        self._y: int
        self._width: int
        self._height: int
        self._bottom: int
        self._right: int

        self._offset = offset
        self._system_measures = system_measures
        self._complete_build()

    def _complete_build(self):
        """
        Internal method!

        Takes given labels and finds bounding box that encapsulates all of them.
        """
        self._x, self._y, self._width, self._height, self._right, self._bottom = find_bbox_for_multiples_bboxs(self._system_measures)
        

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
    
    def __str__(self) -> str:
        output = f"c: system, x: {self._x}, y: {self._y}, w: {self._width}, h: {self._height} \n"
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
    