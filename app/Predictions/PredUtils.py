from ultralytics.engine import results as YOLOresult
from ultralytics.engine.results import Boxes

from .PredLabel import PredLabel


def process_predicted_values(result: YOLOresult, conf=False, threshold: float = 0) -> dict:
    """
    Takes a prediction for single image and returns a dict (JSON-like structure) of predicted boxes.
    Includes image width, height, bounding boxes for each predicted object, may include confidence score,
    all using the standard COCO format.

    Results may be filtered using the `threshold` parameter, all bounding boxes with confidence lower than `threshold`
    will be dropped.

    :param result: prediction result
    :param conf: if true, confidence attribute will be added to each label
    :param threshold: confidence score threshold, all bounding boxes with confidence lower than `threshold`
    will be dropped
    """
    width, height = result.boxes.orig_shape[1], result.boxes.orig_shape[0]
    labels = process_boxes(result.boxes)
    output_classes = [[] for _ in range(len(result.names.keys()))]
    for label in labels:
        if label.conf >= threshold:
            output_classes[label.clss].append(label)
    return construct_final_dict(width, height, output_classes, result.names.values(), conf=conf)


def construct_final_dict(width: int, height: int,
                         sorted_labels: list[list[PredLabel]], class_names: list[str],
                         conf=False) -> dict:
    """
    Constructs final dict for predictions from the YOLO model.

    :param width: width of the original image
    :param height: height of the original image
    :param sorted_labels: sorted list of labels according to their classes
    :param class_names: list of class names
    :param conf: if true, confidence attribute will be added to each label
    """
    output = {"width": width, "height": height}
    for name, labels in zip(class_names, sorted_labels):
        output[name] = []
        for label in labels:
            output[name].append(label.get_coco_to_dict(conf=conf))
    return output


def process_boxes(boxes: Boxes) -> list[PredLabel]:
    """
    Takes in a list of bounding boxes and returns a list of Label objects.

    :param boxes: boxes of ultralytics prediction
    :return: list of Labels that correspond to individual predicted classes
    """
    output: list[PredLabel] = []
    for i in range(len(boxes.cls)):
        center_left, center_top, width, height = boxes.xywh[i]
        left = center_left - width / 2
        top = center_top - height / 2
        output.append(
            PredLabel(int(boxes.cls[i]), int(left), int(top), int(width), int(height), conf=float(boxes.conf[i])))
    return output
