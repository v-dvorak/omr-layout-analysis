import json


class ImageData:
    def __init__(self, doc_id: str, img_id: str, label: str):
        self.source = doc_id
        self.img_id = img_id
        self.label = label

    def __str__(self):
        return f'{self.source} {self.img_id} {self.label}'


class ImageDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageData):
            return {
                "source": obj.source,
                "img_id": obj.img_id,
                "label": obj.label
            }
        return super().default(obj)
