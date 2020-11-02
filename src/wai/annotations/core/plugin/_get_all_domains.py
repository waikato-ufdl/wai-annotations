from functools import lru_cache
from typing import FrozenSet, Type, Optional, Set, Tuple

from ..domain import DomainSpecifier
from ..specifier import *
from ._get_all_plugins_by_type import get_all_plugins_by_type


@lru_cache()
def get_all_domains() -> FrozenSet[Type[DomainSpecifier]]:
    """
    Gets the set of all domains that wai.annotations knows about
    through its plugins.
    """
    # The final set of domains
    translated_domains = set()

    # Get all plugins, categorised by type
    all_plugins_by_base_type = get_all_plugins_by_type()

    # Create a set of domains that haven't been translated yet, starting
    # with all of the input/output domains
    untranslated_domains = set()
    for specifier in all_plugins_by_base_type[SinkStageSpecifier].values():
        untranslated_domains.add(specifier.domain())
    for specifier in all_plugins_by_base_type[SourceStageSpecifier].values():
        untranslated_domains.add(specifier.domain())

    # Keep translating domains until no new ones are found
    first = True  # Python doesn't have a do-loop, so use a flag to indicate the first iteration
    while first or len(untranslated_domains) > 0:
        first = False

        # Translate all the untranslated domains
        new_domains = set()
        for specifier in all_plugins_by_base_type[ProcessorStageSpecifier].values():
            new_domains.update(try_translate_domains(specifier, untranslated_domains)[1])

        # Mark the recently-translated domains as translated
        translated_domains.update(untranslated_domains)

        # The untranslated domains are the new domains which weren't
        # translated previously
        untranslated_domains = new_domains.difference(translated_domains)

    return frozenset(translated_domains)


def try_translate_domains(
        specifier: Type[ProcessorStageSpecifier],
        domains: FrozenSet[Type[DomainSpecifier]]
) -> Tuple[Set[Type[DomainSpecifier]], Set[Type[DomainSpecifier]]]:
    """
    Attempts to translate the given domains using the processor specifier,
    returning the set of successful results.

    :param specifier:   The specifier for a processor stage.
    :param domains:     The domains to translate.
    :return:            The successfully-translated input and output domains.
    """
    # Create the set of successful translations
    successful_input_domains = set()
    successful_output_domains = set()

    # Attempt translation for each domain, adding successes to the set
    for domain in domains:
        translated_domain = try_domain_transfer_function(specifier, domain)
        if translated_domain is not None:
            successful_output_domains.add(translated_domain)
            successful_input_domains.add(domain)

    return successful_input_domains, successful_output_domains


@lru_cache()
def try_domain_transfer_function(
        specifier: Type[ProcessorStageSpecifier],
        domain: Type[DomainSpecifier]
) -> Optional[Type[DomainSpecifier]]:
    """
    Attempts to translate the domain using the given processor specifier,
    returning None if it can't.

    :param specifier:   The specifier for a processor stage.
    :param domain:      The domain to translate.
    :return:            The translate domain or None.
    """
    try:
        return specifier.domain_transfer_function(domain)
    except:
        return None
