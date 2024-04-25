from pathlib import Path
from ..Datasets.OsLiC import OsLiC
from .ImageGen import convert_mscx2format
from .AnnotExtraction.ExtractAnnotations import extract_annotations_from_mscore_svg


def main():
    # Download the OpenScore Lieder dataset
    OsLiC().download_dataset(Path("datasets"))

    # Convert the MSCX files to .png
    path_mscxs = Path("datasets", "Lieder-main", "scores")
    # convert_mscx2format(path_mscxs, "png")  # NOTE: info trva cca 66 minut.

    # Convert the MSCX files to .svg
    # convert_mscx2format(path_mscxs, "svg")  # NOTE: info trva cca 10 minut.

    # Extract the annotations from the SVG
    path_svgs = Path("datasets", "Lieder-main", "scores")
    svg_files = list(path_svgs.glob("**/*.svg"))
    svg_files.sort()  # Sort files if not in the same directory

    for i, svg_file in enumerate(svg_files):
        print(i)
        extract_annotations_from_mscore_svg(  # NOTE: info trva cca 4 hodiny na aic. Vytvoreno 5174 souboru.
            Path(svg_file),
            Path(svg_file.with_suffix(".json"))
        )

    # Convert the annotations to YOLO format
    # path_jsons = Path("datasets", "Lieder-main", "scores")
    # path_jsons = Path("validation_dataset", "annotations")     #TODO: generate eslewhere for eval and val with new yolo/dataset structure
    path_jsons = Path("evaluation_dataset", "annotations")
    json_files = list(path_jsons.glob("**/*.json"))
    json_files.sort()

    for i, json_file in enumerate(json_files):
        print(f"{i}: {json_file}")


if __name__ == "__main__":
    main()
