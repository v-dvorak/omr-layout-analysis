class Label:
    """
    Stores information about a label/annotation in the COCO format.
    """
    def __init__(self, clss: int, x: int, y: int, width: int, height: int):
        self.clss: int = clss
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

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
    
    def get_coco_coordinates(self):
        return [self.x, self.y, self.width, self.height]
    
    def get_coco_label(self):
        """
        Returns label in the COCO format with classification.

        Returns:
        - label in format `[class, x, y, width, height]`
        """
        return [self.clss, *self.get_coco_coordinates()]
    
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

    def to_json(self) -> dict:
        return {
            "left": self.x,
            "top": self.y,
            "width": self.width,
            "height": self.height,
        }
