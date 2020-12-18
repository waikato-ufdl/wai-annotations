# Glossary

Glossary of terminology used in wai-annotations.

**Component** - A single participating element in a pipeline. Can be a source (inserts items into the start of a 
                pipeline), a sink (consumes items from the end of a pipeline), or a processor (an intermediary element
                which performs some operation on the items in the pipeline).

**Conversion Pipeline** - A series of stages comprising a complete conversion sequence, consisting of an input format,
                          a series of intermediate processing stages, and a final output format.
                              
**Cross-Domain Converter (XDC)** - An intermediate processor which converts a dataset from one domain to another.
                                   For example, a video-based domain could be converted to an image-based domain
                                   by treating each frame of the video as an individual image.

**Domain** - A specific type of data, being annotated in a specific manner. For example, datasets
             in the image object-detection domain consist of still images annotated with regions
             containing identified objects.

**Format** - An external representation of a domain. This is typically a way of storing instances of the domain on disk.
             
**Inline Stream Processor (ISP)** - An intermediate processor in the conversion chain, which performs some
                                    mutation of the items in a dataset. ISPs cannot change the domain of a
                                    dataset. For example, an ISP might remove images that are smaller than a
                                    certain size from the conversion stream (for image-based domains).

**Instance** - A specific example of data-item and its annotations in a given domain.

**Macro** - A command-line keyword which is used in place of a series of command-line options. Macros are stored in a
            JSON file, and specified to wai.annotations via the `--macro-file` command-line option.
                                    
**Negative Example** - An item in a dataset which has no annotations. These are typically used when learning to provide
                       examples of what not to look for.
                       
**Plugin** - An implementation of a stage which can be used by wai.annotations to perform some feature. Plugins can be
             specified by external modules via the `wai.annotations.plugins` entry-point in their `setup.py` script.

**Plugin Specifier** - A class which advertises the components that a particular plugin offers for use with
                       wai-annotations.

**Pipeline** - A series of components which process items in their defined order, each passing its output to the next.

**Specifier** - A class used to advertise a stage/domain to wai.annotations from an external module. 

**Splitting** - Because wai.annotations only supports linear pipelines, many formats support splitting of their outputs
                over a number of output directories.

**Stage** - A collection of components which produces, consumes or processes instances.
