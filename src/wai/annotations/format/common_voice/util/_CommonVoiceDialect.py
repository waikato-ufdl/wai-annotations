import csv


class CommonVoiceDialect(csv.Dialect):
    """
    The dialect of Common-Voice TSV files.
    """
    delimiter = '\t'
    quotechar = None
    escapechar = None
    doublequote = None
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE
