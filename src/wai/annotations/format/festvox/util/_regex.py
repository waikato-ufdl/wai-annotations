import re

# The regular expression which matches a single line from a festvox file
LINE_REGEX = '^\\( (?P<filename>.*) "(?P<transcription>.*)" \\)$'

# The compiled regex
LINE_PATTERN = re.compile(LINE_REGEX)
