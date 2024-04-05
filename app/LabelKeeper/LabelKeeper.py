from ..Parser import ParserUtils
from ..Parser import FileUtils

class Label:
    clss: int
    x: int
    y: int
    width: int
    height: int

    def __init__(self, clss: int, x: int, y: int, width: int, height: int):
        self.clss = clss
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        elif self.x != other.x:
            return self.x < other.x
        elif self.width != other.width:
            return self.width < other.width
        else:
            return self.height < other.height

    def __str__(self) -> str:
        return f"c: {self.clss}, x: {self.x}, y: {self.y}, w: {self.width}, h: {self.height}"
    
    def get_coco_label(self):
        return [self.clss, self.x, self.y, self.width, self.height]

class LabelKeeper:

    def __init__(self, labels: list[Label], offset: int = 10) -> None:
        self._system_measures: list[Label] = []  # 0
        self._stave_measures: list[Label] = []   # 1
        self._staves: list[Label] = []           # 2

        self._offset = offset
        self._add_labels(labels)

    def _add_label(self, label: Label):
        all_labels = [self._system_measures, self._stave_measures, self._staves]
        for i in range(len(all_labels)):
            if label.clss == i:
                all_labels[i].append(label)
                break

    def _add_labels(self, labels: list[Label]):
        for label in labels:
            self._add_label(label)
        self._clean_up()
        
    def _clean_up(self):
        all_labels = [self._system_measures, self._stave_measures, self._staves]
        for i in range(len(all_labels)):
            all_labels[i] = ParserUtils.get_unique_list(all_labels[i])
            all_labels[i].sort()

    def __str__(self) -> str:
        all_labels = [self._system_measures, self._stave_measures, self._staves]
        output = ""
        names = ["system_measures", "stave_measures", "staves"]
        for i in range(len(all_labels)):
            output = output + "\n#" + names[i] + "\n"
            for label in all_labels[i]:
                output = output + label.__str__() + "\n"
        return output

class StaveSystem(LabelKeeper):
    _x: int
    _y: int
    _width: int
    _height: int
    _bottom: int
    _right: int
    _avg_stave_height: int

    

    def __init__(self, system_measures: list[Label], offset: int = 10) -> None:
        self._system_measures: list[Label] = []  # 0
        self._stave_measures: list[Label] = []   # 1
        self._staves: list[Label] = []           # 2

        self._offset = offset
        self._system_measures = system_measures
        self.complete_build()

    def complete_build(self):
        
        self._x = min(self._system_measures, key=lambda label: label.x).x
        max_right_measure =  max(self._system_measures, key=lambda label: label.x)
        self._right = max_right_measure.x + max_right_measure.width

        self._y = min(self._system_measures, key=lambda label: label.y).y
        max_down_measure = max(self._system_measures, key=lambda label: label.y)
        self._bottom = max_down_measure.y + max_down_measure.height

        self._width = self._right - self._x
        self._height = self._bottom - self._y

    def is_in(self, label: Label) -> bool:
        return ((self._offset + self._y) < label.x < (self._bottom + self._offset))

    def get_coco_coordinates(self):
        return [self._x, self._y, self._width, self._height]
    
class Sheet(LabelKeeper):
    

    def __init__(self, labels: list[Label], offset: int = 10) -> None:
        self._system_measures: list[Label] = []  # 0
        
        self._stave_measures: list[Label] = []   # 1
        self._staves: list[Label] = []           # 2

        self._stave_systems: list[StaveSystem] = [] # 3 !new in this class!
        
        self._offset = offset
        self._add_labels(labels)
        self._split_into_systems()
    
    def _split_into_systems(self):
        for labels in self._sort_into_bins(self._system_measures):
            self._stave_systems.append(StaveSystem(labels))
    
    def _sort_into_bins(self, labels: list[Label]) -> list[list[Label]]:
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

    def get_all_coco_labels(self):
        all_labels: list[list[Label]] = [self._system_measures, self._stave_measures, self._staves]
        output = []
        
        for labels in all_labels:
            for label in labels:
                output.append(label.get_coco_label())
        
        STAVE_SYSTEM_LABEL = 3
        for label in self._stave_systems:
            output.append([STAVE_SYSTEM_LABEL] + label.get_coco_coordinates())
        
        return output
    
    def get_all_yolo_labels(self, image_width: int, image_height: int):
        # temp = self.get_all_coco_labels()
        output = []
        for label in self.get_all_coco_labels():
            output.append(ParserUtils.coco_to_yolo(label, image_width, image_height))
        return output