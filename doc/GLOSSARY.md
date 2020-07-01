# Glossary

Glossary of terminology used in wai-annotations.

**Conversions Chain** - A series of steps comprising a complete conversion sequence, consisting of an input format, an
                        optional series of intermediate processing stages, and a final output format.
                              
**Cross-Domain Converter (XDC)** - An intermediate processor which converts a dataset from one domain to another.
                                   For example, a video-based domain could be converted to an image-based domain
                                   by treating each frame of the video as an individual image.

**Domain** - A specific type of data, being annotated in a specific manner. For example, datasets
             in the image object-detection domain consist of still images annotated with regions
             containing identified objects.
             
**Inline Stream Processor (ISP)** - An intermediate processor in the conversion chain, which performs some
                                    mutation of the items in a dataset. ISPs cannot change the domain of a
                                    dataset. For example, an ISP might remove images that are smaller than a
                                    certain size from the conversion stream (for image-based domains).
                                    
**Negative Example** - An item in a dataset which has no annotations. These are typically used when learning to provide
                       examples of what not to look for.

**Plugin Specifier** - A class which advertises the components that a particular plugin offers for use with
                       wai-annotations.
