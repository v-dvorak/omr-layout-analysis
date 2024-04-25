import svgelements as sv
from statistics import median

from ...LabelKeeper.Label import Label
from ...Utils.Settings import Settings

################################################
# @author   Kristyna-Harvanova
# @file     extract_annotations_from_mscore_svg.py
# @at       https://github.com/Kristyna-Harvanova/Bachelor-Thesis/
# @license  unspecified
# used with minor tweaks
################################################


def process_staff_lines(
        staff_lines: list
) -> list[Label]:
    # Sort the staff lines by their x and then y coordinate (final order from left to right and from top to bottom).
    staff_lines_sorted = sorted(staff_lines, key=lambda _x: _x.bbox()[0])
    staff_lines_sorted.sort(key=lambda _x: _x.bbox()[1])

    # Merge staff lines that consist of multiple objects.
    staff_lines_final = []
    current_staff_line = staff_lines_sorted[0]
    i = 1
    while i < len(staff_lines_sorted):
        y_diff = staff_lines_sorted[i].bbox()[1] - current_staff_line.bbox()[1]

        # The staff line is the same as the previous, just divided into multiple objects.
        if -1 < y_diff < 1:
            merged_bbox = (
                current_staff_line.bbox()[0],
                current_staff_line.bbox()[1],
                staff_lines_sorted[i].bbox()[2],
                staff_lines_sorted[i].bbox()[3]
            )
            current_staff_line = sv.Polyline(merged_bbox)
        else:
            staff_lines_final.append(current_staff_line)
            current_staff_line = staff_lines_sorted[i]
        i += 1
    staff_lines_final.append(current_staff_line)

    # Calculate the differences between the staff lines and find the average
    differences = [staff_lines_final[i + 1].bbox()[1] - staff_lines_final[i].bbox()[1] for i in
                   range(len(staff_lines_final) - 1)]
    average_diff = median(differences)
    POSSIBLE_SHIFT = 8

    # Cluster staff lines into staves.
    staves = []
    staff = []
    for staff_line in staff_lines_final:
        # If the staff is empty, add the first staff line
        if len(staff) == 0:
            staff.append(staff_line)

        # Add the next staff lines to the staff
        elif len(staff) < 5:
            y_diff = staff_line.bbox()[1] - staff[-1].bbox()[1]
            if average_diff - POSSIBLE_SHIFT < y_diff < average_diff + POSSIBLE_SHIFT:
                staff.append(staff_line)
            else:
                print("Incomplete staff")  # NOTE: This should not happen.

        # If the staff is complete, create a bounding box and reset the staff
        if len(staff) == 5:
            x, y, x_and_width, _ = staff[0].bbox()  # Get the bounding box of the first staff line
            width = x_and_width - x
            height = staff[-1].bbox()[3] - y  # Get the height of the staff = whole 5 lines
            annotation_bbox = Label(Settings.NUMBER_STAVES, int(x), int(y), int(width), int(height))
            staves.append(annotation_bbox)
            staff = []

    return staves
