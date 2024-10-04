import numpy as np
from PIL import Image
from ultralytics import YOLO


def load_model(model_path: str):
    return YOLO(model_path)


def prepare_image(image_path: str):
    image = Image.open(image_path)
    return image, image.size


def prepare_prediction(prediction) -> list[tuple[list[float], float, int]]:
    pred = []
    for i in range(len(prediction.cls)):
        coord = list([float(prediction.xyxy[i][j]) for j in range(len(prediction.xywh[0]))])
        pred.append((
            [coord[0], coord[1], coord[2] - coord[0], coord[3] - coord[1]],
            float(prediction.conf[i]),
            int(prediction.cls[i]) + 1
        ))
    return pred


def get_gt_path(img_path: str) -> str:
    return img_path.replace("images", "labels").replace(".png", ".txt")


def prepare_ground_truth(gt_path: str, width: int, height: int) -> list[tuple[list[float], float, int]]:
    parsed_data = []
    with open(gt_path, 'r') as file:
        for line in file:
            values = line.strip().split()

            # Extract the class (first value)
            class_value = int(values[0])
            x = float(values[1])
            y = float(values[2])
            w = float(values[3])
            h = float(values[4])

            parsed_data.append(([int((x - w / 2) * width), int((y - h / 2) * height), int(w * width), int(h * height)],
                                1.0, class_value + 1))

    return parsed_data
