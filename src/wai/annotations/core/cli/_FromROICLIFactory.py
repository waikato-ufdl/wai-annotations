"""
Automatically generated by gen-cli.py.
"""
from argparse import Namespace
from typing import Type

from wai.common.cli import CLIFactory, CLIInstantiable
from wai.common.meta.typing import VAR_ARGS_TYPE

from wai.common.cli.options._ClassOption import ClassOption


class FromROICLIFactory(CLIFactory):
    """
    Factory which instantiates the FromROI class.
    """
    # Options
    label_mapping = ClassOption('-m', '--mapping', type=str, action='append', help='mapping for labels, for replacing one label string with another (eg when fixing/collapsing labels)', metavar='old=new')

    @classmethod
    def production_class(self, namespace: Namespace) -> Type[CLIInstantiable]:
        from wai.annotations.roi.convert._FromROI import FromROI
        return FromROI

    @classmethod
    def init_args(self, namespace: Namespace) -> VAR_ARGS_TYPE:
        return (namespace,), dict()