from .FileUtils import *  # noqa: F403

def get_unique_list(inp_list: list[any]) -> list[any]:
    """
    Takes a list and returns list of all the unique values
    that were inside given list in the original order.
    Ex: `[8,5,1,3,8,8,4,5,2]` becomes `[8,5,1,3,4,2]`.

    Args:
    - inp_list: input list
    
    Returns:
    - a list in which all values are unique
    """
    unique_list = []
    # got through all elements
    for x in inp_list:
        # check if item is already in list
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

