from ...LabelKeeper.LabelKeeper import Label
from ...Utils.Settings import Settings

################################################
# @author   Kristyna-Harvanova
# @file     extract_annotations_from_mscore_svg.py
# @at       https://github.com/Kristyna-Harvanova/Bachelor-Thesis/
# @license  unspecified
# used with minor tweaks
################################################


def process_bar_lines(
        bar_lines: list,
        staves: list[Label]
) -> list[Label]:
    output = []

    # print(len(bar_lines))
    bar_lines = filter_bars_in_staves(bar_lines, staves)
    # print(len(bar_lines))

    # Sort the bar lines by their x and then y coordinate (final order from left to right and from top to bottom)
    bar_lines_sorted = sorted(bar_lines, key=lambda x: x.bbox()[0])
    bar_lines_sorted.sort(key=lambda x: x.bbox()[1])

    TWO_BARLINE_DIFF = 20  # There can be a measure, that ends with two bar lines, but the space between them is not another measure.
    NEW_STAFF_DIFF = 1.1 * staves[
        0].height  # The minimal space between the staves must be slightly greater than the height of the staff

    # Create a bounding box for each bar
    staff_index = 0
    for i in range(len(bar_lines_sorted)):
        x, y, _, _ = bar_lines_sorted[i].bbox()
        x2, y2, _, _ = bar_lines_sorted[i + 1].bbox() if i + 1 < len(bar_lines_sorted) else (0, 0, 0, 0)

        if (y2 - y) > NEW_STAFF_DIFF:
            staff_index += 1
            # print(f"Throw out staff bcs of y {y2}, {y}")
            continue  # This is not a measure, but a new line = new staff. (Or the end of the score.)
        if x2 - x < TWO_BARLINE_DIFF:
            # print(f"Throw out staff bcs of y {x2}, {x}")
            continue  # This is not a measure, but a double bar line.

        width = x2 - x
        height = staves[staff_index].height
        annotation_bbox = Label(Settings.NUMBER_STAVE_MEASURE, int(x), int(y), int(width), int(height))
        output.append(annotation_bbox)
    # print(len(output))
    return output


def filter_bars_in_staves(
        bar_lines: list,
        staves: list[Label],
        offset: int = 2
):
    output = []
    for bar_line in bar_lines:
        x, y, x1, y1 = bar_line.bbox()
        temp = False
        for staff in staves:
            if y <= staff.y + offset and staff.y + staff.height - offset <= y1:
                bar_line.points = [(x, staff.y), (x1, staff.y + staff.height)]
                output.append(bar_line)
                temp = True
                break
        # if not temp:
        #     print(f"Removing {bar_line.bbox()}")
    return output
