from ..Utils import ParserUtils
from ..Utils.Settings import Settings
from .Label import Label


class LabelKeeper:
    """
    \"Abstract\" class from which all other label-related classes are derived.
    """
    def __init__(self, labels: list[Label], offset: int = 10) -> None:
        """
        Args:
        - labels: labels that will be stored inside this class
        - optional:
            - offset: how far apart two coordinates can be to still be considered the same, in pixels
        """
        # reset lists
        self._system_measures: list[Label] = []  # 0
        self._stave_measures: list[Label] = []   # 1
        self._staves: list[Label] = []           # 2

        self._offset = offset
        self._add_labels(labels)

    def _get_all_labels(self) -> list[list[Label]]:
        """
        Internal method!

        Returns all labels stored inside this class. Should be overridden by subclasses.
        """
        return [self._system_measures, self._stave_measures, self._staves]

    def _add_label(self, label: Label):
        """
        Internal method!

        Adds one label to predefined lists.
        """
        all_labels = self._get_all_labels()
        for i in range(len(all_labels)):
            if label.clss == i:
                all_labels[i].append(label)
                break

    def _add_labels(self, labels: list[Label]):
        """
        Internal method!

        Adds multiple labels to predefined lists.
        """
        for label in labels:
            self._add_label(label)
        self._clean_up()
        
    def _clean_up(self):
        """
        Internal method!

        Makes all lists unique and sorts them.
        This step is necessary for the functionality of the next steps.
        """
        all_labels = [self._system_measures, self._stave_measures, self._staves]
        for i in range(len(all_labels)):
            all_labels[i] = ParserUtils.get_unique_list(all_labels[i])
            all_labels[i].sort()

    def __str__(self) -> str:
        all_labels = [self._system_measures, self._stave_measures, self._staves]
        output = ""
        names = [Settings.NAME_SYSTEM_MEASURE, Settings.NAME_STAVE_MEASURE, Settings.NAME_STAVES]
        for i in range(len(all_labels)):
            output = output + "\n#" + names[i] + "\n"
            for label in all_labels[i]:
                output = output + label.__str__() + "\n"
        return output
