from .LabelKeeper import LabelKeeper
from .Label import Label

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
        self._x = min(self._system_measures, key=lambda label: label.x).x
        # 2
        max_right_measure =  max(self._system_measures, key=lambda label: label.x)
        self._right = max_right_measure.x + max_right_measure.width

        # 3
        self._y = min(self._system_measures, key=lambda label: label.y).y
        # 4
        max_down_measure = max(self._system_measures, key=lambda label: label.y)
        self._bottom = max_down_measure.y + max_down_measure.height

        # | 2 - 1 |
        self._width = self._right - self._x
        # | 4 - 3 |
        self._height = self._bottom - self._y

    def is_in(self, label: Label) -> bool:
        """
        TODO:
        """
        return ((self._offset + self._y) < label.x < (self._bottom + self._offset))

    def get_coco_coordinates(self):
        """
        Returns coordinates encapsulating all given labels in COCO format, without! classification.
        """
        return [self._x, self._y, self._width, self._height]
    
    def __str__(self) -> str:
        return f"c: system, x: {self._x}, y: {self._y}, w: {self._width}, h: {self._height}"