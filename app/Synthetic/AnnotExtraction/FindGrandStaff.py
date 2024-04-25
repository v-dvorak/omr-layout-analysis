import re
import svgelements as sv

from ...LabelKeeper.Label import Label
from ...Utils.Settings import Settings

################################################
# @author   Jirka-Mayer
# @file     find_systems_in_svg_page.py
# @at       https://github.com/ufal/olimpic-icdar24/blob/master/app/datasets/find_systems_in_svg_page.py
# @license  MIT
# used with minor tweaks
################################################


def _svg_path_to_signature(d: str):
    """Replaces numbers with underscores,
    useful for notation object type matching"""
    return re.sub(r"-?\d+(\.\d+)?", "_", d)


PIANO_BRACKET_SIGNATURES = [
    "M_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_",

    "M_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_"
]
NON_PIANO_BRACKET_SIGNATURES = [
    # ensemble bracket body has "points" instead of "d", so "d" is an empty string
    "",

    # ensemble bracket ends have this signature (top end and bottom end)
    "M_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_",
    "M_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_",
    # bracket ends, another variant
    "M_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ C_,_ _,_ _,_ L_,_ L_,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_",
    "M_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_ L_,_ L_,_ L_,_ C_,_ _,_ _,_ L_,_ C_,_ _,_ _,_ C_,_ _,_ _,_ C_,_ _,_ _,_",
]


def process_grand_staff(
        svg_file: sv.SVG,
        bracket_grow=1.1,  # multiplier
):
    # with open(svg_path) as svg_file:
    #     svg_file: SVG = SVG.parse(svg_file, reify=True)

    # vertical pixel ranges (from-to) for system staff_lines
    system_ranges = []
    for element in svg_file.elements():
        if element.values.get("class") == "Bracket":
            signature = _svg_path_to_signature(
                element.values["attributes"].get("d", "")
            )
            if signature in NON_PIANO_BRACKET_SIGNATURES:
                continue
            if signature not in PIANO_BRACKET_SIGNATURES:
                print("UNKNOWN BRACKET:", element.values.get("d", ""))
                print(signature)
                continue

            _, start, _, stop = element.bbox(with_stroke=True)
            height = stop - start
            start -= height * (bracket_grow - 1) / 2
            stop += height * (bracket_grow - 1) / 2
            system_ranges.append((start, stop))
    system_ranges.sort(key=lambda _range: _range[0])

    # check the number is reasonable (these actually occur in the corpus)
    assert len(system_ranges) in [0, 1, 2, 3, 4, 5, 6]

    # sort staff_lines into system bins
    system_staff_lines = [[] for _ in system_ranges]
    for element in svg_file.elements():
        if element.values.get("class") == "StaffLines":
            _, y, _, _ = element.bbox()
            for i, (start, stop) in enumerate(system_ranges):
                if start <= y <= stop:
                    system_staff_lines[i].append(element)

    # get system bounding boxes (tight)
    system_bboxes = [
        sv.Group.union_bbox(staff_lines)
        for staff_lines in system_staff_lines
    ]
    return [Label(Settings.NUMBER_GRAND_STAFF,
                  int(x1), int(y1), int(x2 - x1), int(y2 - y1))
            for x1, y1, x2, y2 in system_bboxes]
