from ..LabelKeeper.Label import Label


class PredLabel(Label):
    def __init__(self, clss: int, x: int, y: int, width: int, height: int, conf: float = None):
        super().__init__(clss, x, y, width, height)
        self.conf: float = conf

    def get_coco_to_dict(self, conf=False):
        """
        Returns label in the COCO format without classification inside a dictionary

        Returns:
        - label in format `{"left": x, "top": y, "width": width, "height": height}`
        with additional `"conf"` parameter if `conf` is True
        """
        output = {}
        for lab, coord in zip(["left", "top", "width", "height"], self.get_coco_coordinates()):
            output[lab] = coord
        if conf:
            output["conf"] = self.conf
        return output
