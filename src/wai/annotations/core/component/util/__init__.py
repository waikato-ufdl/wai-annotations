"""
Utility classes for building conversion components.
"""
from ._AnnotationFileProcessor import AnnotationFileProcessor
from ._Buffer import Buffer
from ._Enumerator import Enumerator
from ._JSONFileWriter import JSONFileWriter
from ._LocalFilenameSource import LocalFilenameSource
from ._LocalFileWriter import LocalFileWriter, ExpectsFile, ExpectsDirectory, iterate_files
from ._SeparateFileWriter import SeparateFileWriter
from ._splitting import SplitSink, SplitState, RequiresNoSplitFinalisation, WithPersistentSplitFiles
from ._WithRandomness import WithRandomness
