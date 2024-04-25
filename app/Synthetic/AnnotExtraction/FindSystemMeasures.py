import svgelements as sv
import numpy as np

from ...LabelKeeper.Label import Label
from ...Utils.Settings import Settings
from ...Utils.LabelUtils import find_bbox_for_multiples_bboxes


def process_system_measures(counts_of_staves_in_system: list[int], staff_measures: list[Label]) -> list[Label]:
    """
    Given list of system measures and how many staves there are in each system on a sheet
    generates a list of system measures.
    """
    """
    Lets' say we have a sheet of music, that has multiple systems A, B, C,
    now each of them has different number of staves. A1, A2, B1, B2, B3, C1, C2.
    
    A1 -------------
    A2 -------------
    
    B1 -------------
    B2 -------------
    B3 -------------
    
    C1 -------------
    C2 -------------
    
    Because all As are in a same system we now that they have the same number of stave measures.
    
    1) We sort all of the stave measures in a sheet by their x coordinate and then by their y coordinate.
    We get a sorted list where the most upper staff is first them and the most left staff measure is first.
    The list looks like this [A1, A2, B1, B2, B3, C1, C2] where A1 are staff measures
    that belong to the first staff etc.
    """
    sorted_staff_measures = sorted(staff_measures, key=lambda label: label.x)
    sorted_staff_measures = sorted(sorted_staff_measures, key=lambda label: label.y)
    """
    2) To be able to separate individual staff measures into staves we need to first count how many staff measures
    are in each line by checking their proximity. Let's say that A, B, C have 4, 5, 3 staff measures respectively.
    Then we get [4, 4, 5, 5, 5, 3, 3] from this proximity check.
    """
    measure_counts_on_line = get_numbers_of_labels_in_same_line(staff_measures)
    """
    4) We take the staff measures and split them by the list of proximity into a list of staves.
    We get a list [staff1 measures, staff2 measures, ...]
    """
    split_to_lines = split_list_by_lengths(sorted_staff_measures, measure_counts_on_line)
    """
    5) Taking the list from the method above we want to get this: [A1, A2, B1, B2, B3, C1, C2], but! we still don't
    precisely where the system measures end. It could also be arranged as [A1, B1, B2, C1, D1, D2, D3] or any other way.
    
    The method is given a list of staff counts in each system on the sheet. In your case, we would get a list
    [2, 3, 2] ~ [(A1, A2), (B1, B2, B3), (C1, C2)]. So we just use the method above and split it again, this time from
    staves in stave systems.
    """
    split_to_system = split_list_by_lengths(split_to_lines, counts_of_staves_in_system)
    """
    6) now we have a list of lists of lists of staff measures. The list looks like this:
    [
        [A1, A2],
        [B1, B2, B3],
        [C1, C2]]
    ]
    Now we just go through the elements each system and link them together (A1[0], A2[0]), (A1[1], A2[1]), ...,
    (B1[0], B2[0], B3[0]), (B1[1], B2[1], B3[1]), ..., (C1[0], C2[0]), (C1[1], C2[1]), ...
    
    At this point we just call a predefined method that finds a bounding box for a list of given Labels and we append
    it to output. 
    """
    bboxes = []
    for i in range(len(split_to_system)):
        measure_collection = np.transpose(split_to_system[i])
        for j in range(len(measure_collection)):
            x, y, width, height, _, _ = find_bbox_for_multiples_bboxes(measure_collection[j])
            bboxes.append(Label(Settings.NUMBER_SYSTEM_MEASURE, x, y, width, height))

    return bboxes


def get_numbers_of_labels_in_same_line(labels: list[Label]) -> list[int]:
    """
    Given a list of labels returns a list of lists of labels that are located at the same height.
    """
    sorted_labels = sorted(labels, key=lambda _label: _label.y)
    output = []

    current_in_line = 0
    current_label = sorted_labels[0]
    for label in sorted_labels:
        if label.y == current_label.y:
            current_in_line += 1
        else:
            output.append(current_in_line)
            current_in_line = 1  # count in the one that we are at right now
            current_label = label
    # finalize
    output.append(current_in_line)
    return output


def split_list_by_lengths(elements: list[any], lengths: list[int]) -> list[list[any]]:
    split_lists = []
    start_index = 0

    for length in lengths:
        split_lists.append(elements[start_index:start_index + length])
        start_index += length

    return split_lists
