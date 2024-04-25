import svgelements as sv

from ...LabelKeeper.Label import Label
from ...Utils.Settings import Settings
from ...Utils.LabelUtils import find_bbox_for_multiples_bboxes


def process_stave_systems(
        bar_lines: list[sv.Polyline],
        staves: list[Label]
) -> (list[Label], list[list[Label]]):
    """
    Given bar lines nad staves finds and returns a list of systems.
    """
    # Sort the bar lines by their x and then y coordinate (final order from left to right and from top to bottom)
    bar_lines_sorted = sorted(bar_lines, key=lambda _x: _x.bbox()[0])
    bar_lines_sorted.sort(key=lambda _x: _x.bbox()[1])

    """
    Systems in a sheet music can be recognized by a line at the beginning of staves that connect all that belong
    to the same system. Unfortunately, in an SVG from MuseScore this line is represented by multiple lines and not
    just one.
    
    From the SVG we extract intervals (top, bottom) of every single bar line. Because we only take a 1D interval, we
    can reduce a list of them into smaller list of longer 1D intervals that do not overlap. Thus we get a list of
    starts and end of staff systems.
    """
    # create intervals
    bar_pool = []
    for bar in bar_lines_sorted:
        _, y1, _, y2 = bar.bbox()
        bar_pool.append((y1, y2))

    # process intervals
    systems_y_coords = reduce_intervals(bar_pool)
    for i in range(len(systems_y_coords)):
        systems_y_coords[i] = (int(systems_y_coords[i][0]), int(systems_y_coords[i][1]))

    # number of intervals correspond to number of systems on a sheet
    systems = [[] for _ in range(len(systems_y_coords))]

    for label in staves:
        sorted_in = False
        for i in range(len(systems_y_coords)):
            if _label_is_in_system(label, systems_y_coords[i]):
                systems[i].append(label)
                sorted_in = True
                break
        if not sorted_in:
            print("Warning! Stave not sorted in a system.")

    output = []
    for i in range(len(systems)):
        x, y, width, height, _, _ = find_bbox_for_multiples_bboxes(systems[i])
        output.append(Label(Settings.NUMBER_SYSTEMS, x, y, width, height))

    return output, systems


def _label_is_in_system(label: Label, system: tuple[int, int], offset=10):
    """
    Returns true if a label is in the system and false otherwise.
    """
    return (label.y > system[0] - offset
            and label.y + label.height < system[1] + offset)


def _is_in_interval(is_in, interval):
    """
    Returns true if interval overlaps with another interval.
    It is supposed that `interval1[0] <= interval2[0]`.
    """
    if interval[0] <= is_in[0] <= interval[1]:
        return True
    else:
        return False


def reduce_intervals(intervals_to_reduce):
    """
    Given a list of interval in the format (start, end) returns a list of reduced intervals that do not overlap.
    """
    intervals_to_reduce = sorted(intervals_to_reduce, key=lambda x: x[0])
    output = []
    current = intervals_to_reduce[0]
    for interval in intervals_to_reduce:
        if _is_in_interval(interval, current):
            current = (current[0], max(current[1], interval[1]))
        else:
            output.append(current)
            current = interval
    # finalize
    output.append(current)

    return output
