"""
Automatically generated by gen-cli.py.
"""
from argparse import Namespace
from typing import Type

from wai.common.cli import CLIFactory, CLIInstantiable
from wai.common.meta.typing import VAR_ARGS_TYPE

from wai.common.cli.options._FlagOption import FlagOption
from wai.common.cli.options._ClassOption import ClassOption


class COCOWriterCLIFactory(CLIFactory):
    """
    Factory which instantiates the COCOWriter class.
    """
    # Options
    license_name = ClassOption('--license-name', type=str, help='the license of the images')
    license_url = ClassOption('--license-url', type=str, help='the license of the images')
    no_images = FlagOption('--no-images', help='skip the writing of images, outputting only the report files')
    output = ClassOption('-o', '--output', type=str, required=True, metavar='dir_or_file')
    pretty = FlagOption('--pretty', help='whether to pretty-print the output')

    @classmethod
    def production_class(self, namespace: Namespace) -> Type[CLIInstantiable]:
        from wai.annotations.coco.io._COCOWriter import COCOWriter
        return COCOWriter

    @classmethod
    def init_args(self, namespace: Namespace) -> VAR_ARGS_TYPE:
        return (namespace,), dict()