from PIL import Image
import numpy as np
import math
from pathlib import Path


def zoom_at_center(img: Image, zoom_factor: float) -> Image:
    """
    Zooms image at center by a given value.

    Parameters
    :param img: image to be zoomed
    :param zoom_factor: zoom factor
    """
    img_width, img_height = img.size

    # dimensions of the crop box
    crop_width = int(img_width / zoom_factor)
    crop_height = int(img_height / zoom_factor)

    # position of the crop box to center the zoom
    left = (img_width - crop_width) // 2
    top = (img_height - crop_height) // 2
    right = (img_width + crop_width) // 2
    bottom = (img_height + crop_height) // 2

    # crop
    cropped_img = img.crop((left, top, right, bottom))
    return cropped_img


def get_histogram(img: Image, color_q_levels: int, space_q_levels: int, normalize: bool = True) -> np.ndarray:
    """
    Returns a black-and-white histogram of the given image.
    Split the image into `space_q_levels` x `space_q_levels`grid
    and for each grid sorts pixels into `color_q_levels` bins.
    By default, the output vector is normalized.

    Parameters
    :param color_q_levels: number of color bins
    :param space_q_levels: grid size
    :param img: input image
    :param normalize: whether to normalize the output vector, default is True
    """
    # b&w histogram
    img = img.convert('L')
    img_pixels = img.getdata()
    height = img.height
    width = img.width

    color_step = 256 / color_q_levels
    x_step = width / space_q_levels
    y_step = height / space_q_levels

    histogramBW = np.array([
        [np.zeros(color_q_levels)
         for _ in range(space_q_levels)] for _ in range(space_q_levels)
    ])

    for y in range(height):
        for x in range(width):
            histogramBW[
                math.floor(x / x_step),
                math.floor(y / y_step),
                math.floor(img_pixels[x + y * width] / color_step)
            ] += 1

    if normalize:
        for i in range(space_q_levels):
            for j in range(space_q_levels):
                histogramBW[i][j] /= np.sum(histogramBW[i][j])

    return histogramBW.flatten()


def combine_images_into_grid(image_paths: list[str | Path],
                             m: int, n: int, size: tuple[int, int] = (100, 100),
                             output_path: str | Path = None):
    """
    Combines images into a m x n grid and show the result.
    If output path is not specified, methods shows the final image on screen.

    :param image_paths: list of image paths to combine
    :param m: number of rows in the grid
    :param n: number of columns in the grid
    :param size: size of image in grid in pixels
    :param output_path: path to output image
    """

    # ensure there are enough images to fill the grid
    if len(image_paths) < m * n:
        raise ValueError(f"Not enough images to fill a {m}x{n} grid")

    img_width, img_height = size
    grid_img = Image.new('RGB', (n * img_width, m * img_height))

    for idx, img_path in enumerate(image_paths[:m * n]):
        img = Image.open(img_path).resize((img_width, img_height))

        # positioning
        row = idx // n
        col = idx % n
        x = col * img_width
        y = row * img_height

        # paste image into grid
        grid_img.paste(img, (x, y))

    if output_path is not None:
        grid_img.save(output_path)
    else:
        grid_img.show()
