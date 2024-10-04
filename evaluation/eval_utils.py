from __future__ import annotations
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

from PIL import Image
from PIL import Image, ImageDraw, ImageFont

import os
import cv2

font_path = os.path.join(cv2.__path__[0], 'qt', 'fonts', 'DejaVuSans.ttf')


def box_to_coco_format(box):
    """
    Convert (top, left, bottom, right) to (left, top, width, height)
    """
    top, left, bottom, right = box
    width = right - left
    height = bottom - top
    return [left, top, width, height]


def prepare_coco_format(gt_data: list[list[tuple[tuple[float, float, float, float], float, int]]],
                        pred_data: list[list[tuple[tuple[float, float, float, float], float, int]]],
                        classes: list[str]):
    """
    Input data format: ((left, top, width, height), certainty, class), coordinates are absolute.
    """
    coco_ground_truth = {
        "images": [{"id": img_id} for img_id in range(len(gt_data))],  # Image IDs for all images
        "annotations": [],
        "categories": [{"id": cls_id, "name": cls_name} for cls_id, cls_name in enumerate(classes, 1)],
    }

    coco_predictions = []
    annotation_id = 0

    # Add ground truth annotations for each image
    for img_id, gt_boxes in enumerate(gt_data):
        for box, certainty, clss in gt_boxes:
            coco_ground_truth["annotations"].append({
                "id": annotation_id,
                "image_id": img_id,  # assign image ID
                "category_id": clss,  # multiple classes
                "bbox": box,
                "area": box[2] * box[3],  # area of the bbox
                "iscrowd": 0
            })
            annotation_id += 1

    # Add predictions for each image
    for img_id, pred_boxes in enumerate(pred_data):
        for box, certainty, clss in pred_boxes:
            coco_predictions.append({
                "image_id": img_id,  # Assign image ID
                "category_id": clss,  # Multiple classes
                "bbox": box,
                "score": certainty
            })

    return coco_ground_truth, coco_predictions


def evaluate_metrics(gt_data, pred_data, classes):
    coco_gt_data, coco_pred_data = prepare_coco_format(gt_data, pred_data, classes)

    # Create COCO ground truth object
    coco_gt = COCO()
    coco_gt.dataset = coco_gt_data
    coco_gt.createIndex()

    # Create COCO predictions object (simulates the result file)
    coco_dt = coco_gt.loadRes(coco_pred_data)

    # Evaluate using COCOeval
    coco_eval = COCOeval(coco_gt, coco_dt, 'bbox')
    coco_eval.params.imgIds = list(range(len(gt_data)))  # Evaluate all image IDs
    coco_eval.evaluate()
    coco_eval.accumulate()
    print(f"=== Total Metrics (all images and classes combined) ===")
    coco_eval.summarize()

    # Per-class metrics
    for class_id, class_name in enumerate(classes, 1):
        coco_eval.params.catIds = [class_id]  # Filter by class
        coco_eval.evaluate()
        coco_eval.accumulate()
        print(f"\n=== Metrics for class: {class_name} ===")
        coco_eval.summarize()


def draw_rectangles(image_path, coordinates: list[tuple[tuple[float, float, float, float], float, int]], classes: int,
                    threshold: float = 0.5):
    """
    Draws rectangles on the image based on absolute coordinates. Expects COCO format (left, top, width, height).

    Mainly used for debugging.
    """
    for current_cls in range(classes):
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        for dat in coordinates:
            if dat[2] - 1 == current_cls and dat[1] > threshold:
                (left, top, widht, height) = dat[0]
                # Scale the coordinates based on the image size
                top_pixel = int(top)
                left_pixel = int(left)
                bottom_pixel = int(top + height)
                right_pixel = int(left + widht)

                # Draw a rectangle (outline only)
                draw.rectangle([left_pixel, top_pixel, right_pixel, bottom_pixel], outline="red", width=2)

        print(f"saving {current_cls}")
        img.save(f"eval_tests/{current_cls}.png")


def draw_rectangles_with_conf(image_path, coordinates: list[tuple[tuple[float, float, float, float], float, int]],
                              classes: int, threshold: float = 0.5):
    """
    Draws rectangles on the image based on absolute coordinates and displays confidence.
    Expects coordinates in COCO format (left, top, width, height), with confidence and class info.
    """

    # Load a font (optional, you can specify a font path if desired)
    # font = ImageFont.load_default()
    font = ImageFont.truetype(font_path, size=25)

    for current_cls in range(classes):
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        for dat in coordinates:
            # dat[0]: (left, top, width, height)
            # dat[1]: confidence score
            # dat[2]: class label (subtract 1 as per the existing code)

            if dat[2] - 1 == current_cls and dat[1] > threshold:
                (left, top, width, height) = dat[0]
                confidence = dat[1]

                # Scale the coordinates based on the image size
                top_pixel = int(top)
                left_pixel = int(left)
                bottom_pixel = int(top + height)
                right_pixel = int(left + width)

                # Draw the main rectangle (outline only)
                draw.rectangle([left_pixel, top_pixel, right_pixel, bottom_pixel], outline="red", width=2)

                # Create a filled rectangle for the confidence label at the top-left of the main rectangle
                label_height = 30  # Fixed height for the label box
                label_width = 80  # Width of the label box for the confidence text
                draw.rectangle([left_pixel, top_pixel, left_pixel + label_width, top_pixel + label_height], fill="red")

                # Draw the confidence score inside the label box
                draw.text((left_pixel + 5, top_pixel), f"{confidence:.3f}", fill="white", font=font)

        print(f"saving {current_cls}")
        img.save(f"{image_path}_{current_cls}.png")