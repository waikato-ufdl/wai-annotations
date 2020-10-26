from abc import ABC
from random import Random
from typing import Optional

from wai.common.cli.options import TypedOption, Option

from ...util import InstanceState
from .._Component import Component


class WithRandomness(Component, ABC):
    """
    Adds a seed option to a component, and automatically provides
    a source of randomness for instances to use.
    """
    # The seed to use for randomisation of the read sequence
    seed = TypedOption(
        "--seed",
        type=int
    )

    @property
    def has_random(self):
        """
        Whether a seed was provided.
        """
        return self.random is not None

    @InstanceState
    def random(self) -> Optional[Random]:
        """
        The source of randomness for this reader. Used for randomising the read order
        of annotation/data files.
        """
        return None if self.seed is None else Random(self.seed)

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.seed:
            return cls.get_help_text_for_seed_option()
        return super().get_help_text_for_option(option)

    @classmethod
    def get_help_text_for_seed_option(cls) -> str:
        return "the seed to use for randomisation"
