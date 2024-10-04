from __future__ import annotations

import argparse
import random
from glob import glob

from tqdm import tqdm

import eval_utils
import yolo_utils

CLASSES = ["system_measures", "stave_measures", "staves", "systems", "grand_staff"]


def yolo_pred_gt_job(model_path: str, val_dir: str, count: int, seed: int = 42) -> tuple[
    list[list[tuple[list[float], float, int]]], list[list[tuple[list[float], float, int]]]
]:
    model = yolo_utils.load_model(model_path)
    images = list(glob(val_dir + "/*.png"))

    if count is not None:
        random.Random(seed).shuffle(images)
        images = images[:count]

    ground_truths = []
    predictions = []

    for image in tqdm(images):
        im, (width, height) = yolo_utils.prepare_image(image)

        prediction = model.predict(source=im)[0]

        predictions.append(yolo_utils.prepare_prediction(prediction.boxes))
        ground_truths.append(yolo_utils.prepare_ground_truth(yolo_utils.get_gt_path(image), width, height))

    return ground_truths, predictions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate TensorFlow object detection model on a validation dataset.")
    parser.add_argument("model_path", type=str, help="Path to model.")
    parser.add_argument("dataset_dir", type=str, help="Path to validation dataset.")
    parser.add_argument("-c", "--count", type=int, help="How many images the model will be tested on.")
    parser.add_argument("-s", "--seed", type=int, default=42, help="Seed for dataset shuffling.")
    args = parser.parse_args()

    GROUND_TRUTH, PREDICTIONS = yolo_pred_gt_job(args.model_path, args.dataset_dir, args.count, seed=int(args.seed))

    eval_utils.evaluate_metrics(GROUND_TRUTH, PREDICTIONS, CLASSES)
