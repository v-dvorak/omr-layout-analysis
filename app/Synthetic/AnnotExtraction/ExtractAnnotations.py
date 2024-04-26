import json
import svgelements as sv
from pathlib import Path

from ...Utils.Settings import Settings
from .FindSystems import process_stave_systems
from .FindStaffLines import process_staff_lines
from .FindStaffMeasures import process_bar_lines
from .FindGrandStaff import process_grand_staff
from .FindSystemMeasures import process_system_measures

################################################
# @author   Kristyna-Harvanova
# @file     extract_annotations_from_mscore_svg.py
# @at       https://github.com/Kristyna-Harvanova/Bachelor-Thesis/
# @license  unspecified
# used with minor tweaks
################################################


def extract_annotations_from_mscore_svg(
        from_path_svg: Path,
        to_path_json: Path
):
    # Load the SVG file
    with open(from_path_svg) as svg_file:
        svg_file: sv.SVG = sv.SVG.parse(svg_file, reify=True)

    svg_info = {}

    wanted_classes = ["StaffLines", "BarLine"]

    staff_lines = []
    bar_lines = []

    # Extract the information from the SVG file
    for element in svg_file.elements():
        if type(element) is sv.SVG:
            width = round(float(element.values.get("width").replace("px", "")))
            height = round(float(element.values.get("height").replace("px", "")))

            svg_info["width"] = width
            svg_info["height"] = height

        elif type(element) is sv.Path or type(element) is sv.Polyline:
            cls = element.values.get('class', '')
            if cls not in wanted_classes:
                continue

            if cls == "StaffLines":
                staff_lines.append(element)
            elif cls == "BarLine":
                bar_lines.append(element)

    # Default empty values if page is empty / background
    staves = []
    bar_lines_final = []
    systems = []
    grand_staff = []
    system_measures = []

    # Process the staff lines
    if len(staff_lines) > 0:
        staves = process_staff_lines(staff_lines)

        systems, system_info = process_stave_systems(bar_lines, staves)
        bar_lines_final = process_bar_lines(bar_lines, staves)
        grand_staff = process_grand_staff(svg_file)
        # process system measures:
        staff_count = [len(x) for x in system_info]
        system_measures = process_system_measures(staff_count, bar_lines_final)

    # Add the annotations to the SVG info
    svg_info[Settings.NAME_STAVES] = [x.to_json() for x in staves]
    svg_info[Settings.NAME_STAVE_MEASURE] = [x.to_json() for x in bar_lines_final]
    svg_info[Settings.NAME_SYSTEMS] = [x.to_json() for x in systems]
    svg_info[Settings.NAME_GRAND_STAFF] = [x.to_json() for x in grand_staff]
    svg_info[Settings.NAME_SYSTEM_MEASURE] = [x.to_json() for x in system_measures]

    # Save the information to a JSON file
    with open(to_path_json, "w") as json_file:
        json.dump(svg_info, json_file, indent=4)
