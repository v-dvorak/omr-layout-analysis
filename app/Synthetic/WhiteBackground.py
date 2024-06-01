from PIL import Image
from pathlib import Path
from tqdm import tqdm


def add_white_background(image_path, output_path, verbose: bool = False):
    """
    Adds a white background to a PNG image with a transparent background.

    :param image_path: path to the input image
    :param output_path: path to save the output
    :param verbose: make script verbose
    """
    img = Image.open(image_path).convert("RGBA")

    # new image with a white background
    white_bg = Image.new("RGBA", img.size, "WHITE")
    # composite the original onto the background
    combined_img = Image.alpha_composite(white_bg, img)
    # convert to RGB mode, remove the alpha channel
    final_img = combined_img.convert("RGB")
    final_img.save(output_path)

    if verbose:
        print(f"Image saved to {output_path}")


def process_directory(input_dir: Path):
    """
    Processes all PNG images in the input directory, adding a white background,
    replace the version with a new one.

    :param input_dir: Directory containing the input PNG images
    """
    # Iterate over all files in the input directory
    for img_path in tqdm(list(input_dir.rglob("*.png"))):
        input_path = img_path
        output_path = img_path
        add_white_background(input_path, output_path)


if __name__ == "__main__":
    DATASET_DIR = Path("datasets/Lieder-main/scores")
    process_directory(DATASET_DIR)
