from typing import Type, List

from ..domain import DomainSpecifier
from ..specifier import StageSpecifier, SourceStageSpecifier, SinkStageSpecifier, ProcessorStageSpecifier
from ._get_all_domains import get_all_domains, try_translate_domains


def get_plugin_domains(plugin: Type[StageSpecifier]) -> List[Type[DomainSpecifier]]:
    """
    Gets a list of the domains that a plugin can participate in.

    :param plugin:
                The plugin specifier.
    :return:
                The list of domains.
    """
    if issubclass(plugin, SourceStageSpecifier):
        return [plugin.domain()]
    elif issubclass(plugin, SinkStageSpecifier):
        return [plugin.domain()]
    elif issubclass(plugin, ProcessorStageSpecifier):
        return list(try_translate_domains(plugin, get_all_domains())[0])

    assert False, f"plugin {plugin} is an unknown type of stage specifier"
