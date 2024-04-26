from pathlib import Path
from tqdm import tqdm
import json
import sys

from ..Datasets.Oslic import OsLiC
from .ImageGen import convert_mscx2format
from .AnnotExtraction.ExtractAnnotations import extract_annotations_from_mscore_svg
from .BanProcessor import BanProcessor
from ..Utils import ParserUtils


def main():
    # DATASET DOWNLOAD
    OsLiC().download_dataset(Path("datasets"))
    oslic_path_mscxs = Path("datasets", "Lieder-main", "scores")

    # PROCESS ARGUMENTS
    # load arguments and flags
    mscxs_to_process = []
    args = sys.argv[1:]
    file_names = [arg for arg in args if (not arg.startswith("--") and not arg.startswith("-"))]

    # check verbose, png, svg
    PROCESS_PNG = False
    PROCESS_SVG = False
    VERBOSE = False
    if "--png" in args:
        PROCESS_PNG = True
    if "--svg" in args:
        PROCESS_SVG = True
    if "-v" in args or "--verbose" in args:
        VERBOSE = True

    # load files
    print("Loading documents to process:")
    if len(file_names) == 0:
        print("⚠️ No file names provided, all files will be loaded and processed.")
        mscxs_to_process = list(oslic_path_mscxs.rglob("*.mscx"))
    else:
        for file in file_names:
            found_files = list(oslic_path_mscxs.rglob("*" + file.split("-")[0] + ".mscx"))
            if len(found_files) == 0:
                print(f"⚠️ {file} was not found.")
            else:
                mscxs_to_process += found_files
        if len(mscxs_to_process) == 0:
            print("❗ No mscxs were found, quitting job.")
            quit()
        elif VERBOSE:
            print("Loaded files:")
            total = len(mscxs_to_process)
            for i, file in enumerate(mscxs_to_process):
                print(f"{i+1}/{total}: {file}")

    # BANNED SCORES REMOVAL
    print("Removing globally ignored scores:")
    mscx_paths = []
    ban_hammer = BanProcessor()
    for i in tqdm(range(len(mscxs_to_process))):
        if ban_hammer.is_banned_document(mscxs_to_process[i]):
            continue
        else:
            mscx_paths.append(mscxs_to_process[i])
    if len(mscx_paths) == 0:
        print("❗ All scores specified are banned, quitting job.")
        quit()

    # MSCX CONVERSION
    # Convert the MSCX files to .png
    if PROCESS_PNG:
        print("Converting scores to PNGs:")
        tqdm(convert_mscx2format(mscx_paths, oslic_path_mscxs, "png"))  # NOTE: info trva cca 66 minut.

    # Convert the MSCX files to .svg
    if PROCESS_SVG:
        print("Converting scores to SVGs:")
        tqdm(convert_mscx2format(mscx_paths, oslic_path_mscxs, "svg"))  # NOTE: info trva cca 10 minut.

    # LOAD PROCESSED SVGS
    print("Loading pages to process:")
    svgs_to_process = []
    if not file_names:
        svgs_to_process = list(oslic_path_mscxs.rglob("*.svg"))
    else:
        for file in file_names:
            found_files = list(oslic_path_mscxs.rglob(f"*{file}*.svg"))
            if len(found_files) == 0:
                print(f"⚠️ The page of {file} you specified does not exist.")
            else:
                svgs_to_process += found_files
        if len(svgs_to_process) == 0:
            print("❗ No svgs were found, quitting job.")
            quit()
        elif VERBOSE:
            print("Loaded music sheets:")
            total = len(svgs_to_process)
            for i, file in enumerate(svgs_to_process):
                print(f"{i+1}/{total}: {file}")

    # BANNED SCORES REMOVAL
    print("Removing globally ignored pages:")
    svg_paths = []
    for i in tqdm(range(len(svgs_to_process))):
        if ban_hammer.is_banned_page(svgs_to_process[i]):
            continue
        else:
            svg_paths.append(svgs_to_process[i])
    if len(svg_paths) == 0:
        print("❗ All pages specified are banned, quitting job.")
        quit()

    # EXTRACT ANNOTATIONS
    print("Extracting annotations:")
    svg_paths.sort()  # Sort files if not in the same directory

    total = len(svg_paths)
    for i in tqdm(range(total), disable=VERBOSE):
        print(i)
        svg_file = svg_paths[i]
        if VERBOSE:
            print(f"{i+1}/{total} Extracting from: {svg_file}", end="")
        try:
            extract_annotations_from_mscore_svg(  # NOTE: info trva cca 4 hodiny na aic. Vytvoreno 5174 souboru.
                Path(svg_file),
                Path(svg_file.with_suffix(".json"))
            )
            if VERBOSE:
                print(" ✅ ")
        except Exception as e:
            ParserUtils.print_parsing_error(svg_file, e, i + 1, total)


if __name__ == "__main__":
    main()
