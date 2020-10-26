from typing import Iterable, Tuple, Optional

from .util import *
from ._StreamProcessor import StreamProcessor
from ._StreamSink import StreamSink
from ._StreamSource import StreamSource
from ._typing import ThenFunction


class Pipeline:
    """
    A pipeline of sequential stream-processors, optionally capped
    by a source and/or sink.
    """
    def __init__(self,
                 source: Optional[StreamSource] = None,
                 processors: Iterable[StreamProcessor] = tuple(),
                 sink: Optional[StreamSink] = None):
        # The optional source of the stream
        self._source: Optional[StreamSource] = source

        # The processors in order of application
        self._processors: Tuple[StreamProcessor, ...] = tuple(processors)

        # The optional consumer of the stream
        self._sink: Optional[StreamSink] = sink

    @property
    def has_source(self):
        """
        Whether this pipeline has a fixed source.
        """
        return self._source is not None

    @property
    def source(self) -> StreamSource:
        """
        The source of this pipeline.
        """
        if not self.has_source:
            raise Exception("No source")
        return self._source

    @property
    def processors(self) -> Tuple[StreamProcessor, ...]:
        """
        The stream processors in this pipeline, in order of application.
        """
        return self._processors

    @property
    def has_sink(self):
        """
        Whether this pipeline has a fixed sink.
        :return:
        """
        return self._sink is not None

    @property
    def sink(self) -> StreamSink:
        """
        The sink of this pipeline.
        """
        if not self.has_sink:
            raise Exception("No sink")
        return self._sink

    def process(self,
                source: Optional[Iterable] = None,
                sink: Optional[ThenFunction] = None):
        """
        Executes this pipeline.

        :param source:  The source to provide stream elements to the pipeline.
                        Uses the fixed source if none given.
        :param sink:    The sink to consume the stream elements.
                        Uses the fixed sink if none given.
        """
        # Use the provided sink function, or the fixed sink if none given
        if sink is None:
            sink = self.sink
        else:
            sink = FunctionStreamSink(sink)

        # Use the provided source iterable, or the fixed source if none given
        if source is None:
            source = self.source
        else:
            source = IterableStreamSource(source)

        # Make sure all process state is reset
        reset_all_process_state(source, *self.processors, sink)

        # Start the sink
        sink.start()

        # Start building the functional pipeline from the sink backwards
        pipeline = sink.consume_element, sink.finish

        # Start and attach each processor in turn
        for processor in reversed(self.processors):
            processor.start()
            pipeline = enforce_calling_semantics(
                processor.process_element,
                processor.finish,
                then=pipeline[0],
                done=pipeline[1]
            )

        # Attach the source
        pipeline = enforce_calling_semantics(
            source.produce,
            then=pipeline[0],
            done=pipeline[1]
        )

        # Execute the pipeline
        try:
            pipeline[0]()
        finally:
            # Tidy up all process state
            reset_all_process_state(source, *self.processors, sink)
