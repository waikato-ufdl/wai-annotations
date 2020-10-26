import os
from abc import abstractmethod, ABC
from typing import TypeVar, Dict, Tuple, Optional, Callable, Any, Generic, ContextManager, Iterable

from contextlib2 import ExitStack

from wai.bynning.operations import split as bynning_split_op

from wai.common.cli.options import TypedOption

from ...stream.util import ProcessState
from ...util import InstanceState, StateType, ReentrantContextManager, gcd
from .._SinkComponent import SinkComponent
from ._LocalFileWriter import LocalFileWriter

ElementType = TypeVar("ElementType")


class SplitSink(SinkComponent[ElementType], ABC):
    """
    Base class for classes which can write a specific external format.
    """
    split_names = TypedOption(
        "--split-names",
        type=str,
        metavar="SPLIT NAME",
        nargs="+",
        help="the names to use for the splits"
    )

    split_ratios = TypedOption(
        "--split-ratios",
        type=int,
        metavar="RATIO",
        nargs="+",
        help="the ratios to use for the splits"
    )

    def start(self):
        super().start()
        if isinstance(self, LocalFileWriter):
            self.create_split_directories(self.output_path)

    def consume_element(self, element: ElementType):
        self.consume_element_for_split_with_exit_stack(element)
        self._move_to_next_split()

    def consume_element_for_split_with_exit_stack(self, element: ElementType):
        if isinstance(self, WithPersistentSplitFiles):
            with self._exit_stack:
                self.consume_element_for_split(element)
        else:
            self.consume_element_for_split(element)

    @abstractmethod
    def consume_element_for_split(self, element: ElementType):
        raise NotImplementedError(self.consume_element_for_split.__qualname__)

    def finish(self):
        try:
            # If we're not splitting, just finish the None split
            if not self.is_splitting:
                return self.finish_split_with_exit_stack()

            # Create a set of finished splits so we don't finish each more than once
            finished_splits = set()

            # Manually move through the splits so we only pass once
            split_index = 0

            # Finish each split
            while split_index < len(self.split_schedule):
                # Manually move to the indexed split
                self.split_index = split_index

                # Finish this split if we haven't already
                if self.split_label not in finished_splits:
                    self.finish_split_with_exit_stack()
                    finished_splits.add(self.split_label)

                # Move on to the next split in the schedule
                split_index += 1

        finally:
            if isinstance(self, WithPersistentSplitFiles):
                self._exit_stack.finish()

    def finish_split_with_exit_stack(self):
        if isinstance(self, WithPersistentSplitFiles):
            with self._exit_stack:
                self.finish_split()
        else:
            self.finish_split()

    @abstractmethod
    def finish_split(self):
        raise NotImplementedError(self.finish_split.__qualname__)

    def create_split_directories(self, base_path: str):
        split_names = (None,) if len(self.split_table) == 0 else self.split_table.keys()
        for split_name in split_names:
            os.makedirs(self.get_split_path(split_name, base_path), exist_ok=True)

    @staticmethod
    def get_split_path(split_name: Optional[str], path: str, is_filename: bool = False) -> str:
        """
        Formats the path for a split.

        :param split_name:      The name of the split, or None for no split.
        :param path:            The base path.
        :param is_filename:     Whether the given path is a filename or directory name.
        :return:                The path for the split.
        """
        # Use the given path if no split-name is given
        if split_name is None:
            return path

        if is_filename:
            directory, filename = os.path.split(path)
            return os.path.join(directory, split_name, filename)
        else:
            return os.path.join(path, split_name)

    @property
    def is_splitting(self) -> bool:
        """
        Whether this writer is performing a split-write.
        """
        return len(self.split_names) != 0 and len(self.split_ratios) != 0

    @InstanceState
    def split_table(self) -> Dict[Optional[str], int]:
        """
        Table from split name to split ratio.
        """
        # If we're not splitting, create a default table
        if not self.is_splitting:
            return {None: -1}

        # Create a table from split-name to split-ratio
        table = {
            split_name: split_ratio
            for split_name, split_ratio
            in zip(self.split_names, self.split_ratios)
        }

        # Reduce each ratio to its lowest form
        table_gcd = gcd(*table.values())
        for split_name in table:
            table[split_name] //= table_gcd

        return table

    @InstanceState
    def split_schedule(self) -> Tuple[str, ...]:
        """
        Creates a schedule of which split to assign elements to
        in order of discovery.
        """
        # If we're not splitting, return an empty schedule
        if not self.is_splitting:
            return tuple()

        # Calculate a range over the length of the schedule
        schedule_range = range(sum(self.split_table.values()))

        # Create a mapping from split-name to schedule indices
        split_indices_by_name = {
            split_name: set(split_indices)
            for split_name, split_indices
            in bynning_split_op(schedule_range, **self.split_table).items()
        }

        return tuple(
            split_name
            for split_name, split_indices in split_indices_by_name.items()
            for index in schedule_range
            if index in split_indices
        )

    split_index: int = ProcessState(lambda self: 0 if self.is_splitting else -1)

    @property
    def split_label(self) -> Optional[str]:
        if not self.is_splitting:
            return None
        return self.split_schedule[self.split_index]

    def _move_to_next_split(self):
        if not self.is_splitting:
            return
        self.split_index = (self.split_index + 1) % len(self.split_schedule)


class SplitState(ProcessState[StateType]):
    """
    Class that initialises state for each individual split.
    """
    def __init__(self, initialiser: Callable[[Any], StateType]):
        super().__init__(lambda self: {})
        self._split_initialiser: Callable[[Any], StateType] = initialiser

    def __get__(self, instance: SplitSink, owner: type) -> StateType:
        # Get the state for all splits
        splits_state = super().__get__(instance, owner)

        # If it's not the state (i.e. it is the descriptor) just return it
        if not isinstance(splits_state, dict):
            return splits_state

        # Get the current split label
        split_label = instance.split_label

        # Initialise the state for this split if not already
        if split_label not in splits_state:
            splits_state[split_label] = self._split_initialiser(instance)

        return splits_state[split_label]

    def __set__(self, instance: SplitSink, value: StateType):
        # Get the state for all splits
        splits_state = super().__get__(instance, type(instance))

        # Get the current split label
        split_label = instance.split_label

        # Set the value for this split
        splits_state[split_label] = value


class RequiresNoSplitFinalisation:
    """
    Mixin class for declaring that a SplitSink doesn't need to
    finalise it's splits.
    """
    def finish_split(self):
        pass


SplitFilesType = TypeVar("SplitFilesType")


class WithPersistentSplitFiles(Generic[SplitFilesType]):
    """
    Mixin class which handles the opening/closing of files for split-sinks which
    need to keep files open for each split during processing.
    """
    # The exit stack which manages the files
    _exit_stack: ExitStack = ProcessState(lambda self: ReentrantContextManager(ExitStack()))

    # The split files
    _split_files: SplitFilesType = SplitState(lambda self: self.__init_split_files_actual())

    def __init_split_files_actual(self) -> SplitFilesType:
        split_files = self._init_split_files()
        iterator = self._iterate_split_files(split_files)
        with self._exit_stack as exit_stack:
            for split_file in iterator:
                exit_stack.enter_context(split_file)
        return split_files

    @abstractmethod
    def _init_split_files(self) -> SplitFilesType:
        """
        Initialises the files for this split.

        :return:    The files.
        """
        raise NotImplementedError(self._init_split_files.__qualname__)

    @abstractmethod
    def _iterate_split_files(self, split_files: SplitFilesType) -> Iterable[ContextManager]:
        """
        Should iterate through all files in the split files.

        :param split_files:     The files for this split.
        :return:                An iterator over those files.
        """
        raise NotImplementedError(self._iterate_split_files.__qualname__)
