from ..LabelKeeper.Label import Label


def find_bbox_for_multiples_bboxes(labels: list[Label]):
    """
    Given a bunch of rectangles we need to find the "most-left", "most-up", etc.
    points.

    +→ x
    ↓
    y
        3
        |
    1---+-------+---2
                |
                4
    """
    # 1
    x = min(labels, key=lambda label: label.x).x
    # 2
    max_right_measure = max(labels, key=lambda label: label.x)
    right = max_right_measure.x + max_right_measure.width

    # 3
    y = min(labels, key=lambda label: label.y).y
    # 4
    max_down_measure = max(labels, key=lambda label: label.y)
    bottom = max_down_measure.y + max_down_measure.height

    # | 2 - 1 |
    width = right - x
    # | 4 - 3 |
    height = bottom - y

    return (x, y, width, height, right, bottom)
