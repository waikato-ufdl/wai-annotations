from abc import abstractmethod
from typing import List, Tuple

from ...stream import ThenFunction, DoneFunction
from ...stream.util import ProcessState

from .._ProcessorComponent import ProcessorComponent


class GroupFilenames(ProcessorComponent[Tuple[str, bool], Tuple[str, List[str]]]):
    """
    Processor which groups file-names by some criteria.
    """
    groups = ProcessState(lambda self: {})

    @abstractmethod
    def assign_group(self, filename: str) -> str:
        """
        Assigns a group to the file-name.

        :param filename:    The filename to assign.
        :return:            The group name.
        """
        raise NotImplementedError(self.assign_group.__qualname__)

    def process_element(
            self,
            element: Tuple[str, bool],
            then: ThenFunction[Tuple[str, List[str]]],
            done: DoneFunction
    ):
        # Extract the file-name
        filename, _ = element

        # Assign this file-name to a group
        group = self.assign_group(filename)

        # Add the file-name to its group
        groups = self.groups
        if group not in groups:
            groups[group] = [element]
        else:
            groups[group].append(element)

    def finish(
            self,
            then: ThenFunction[Tuple[str, List[str]]],
            done: DoneFunction
    ):
        # Forward each of the groups
        for mapping in self.groups.items():
            then(mapping)

        done()
