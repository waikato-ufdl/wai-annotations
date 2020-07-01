# Adding Components to Wai-Annotations Through Plugins

wai-annotations uses a plugin system to allow other libraries to add new processing components
without modifying the base library source. This document details how to go about using this system.

## Plugin Types

There are 4 types of components which can be added to wai-annotations via plugin: input formats, ISPs, XDCs and output
formats. New domains can also be added, but these are specified indirectly via any of the previous components.

## Domains

New domains are added indirectly to wai-annotations as dependencies of components, as a domain which has no components
is essentially unreachable to a conversion chain. However the specification of new domains is treated as a
plugin-related issue, so it is detailed here.

A domain is essentially the definition of an instance format, which contains both an item in the conversion dataset and
the annotations attached to that item. The actual item in the dataset is represented by a `FileInfo` object, which
contains the name of the item, and the binary data blob containing the item's file data. Domains need to specify a
sub-class of `FileInfo` to represent the item and any additional data about it. The annotations for an instance can be
any arbitrary type.

To specify a new domain, a domain specifier must be created. This is achieved by importing the base classes from the
core wai-annotations package and implementing the abstract methods.

```python
from typing import Type

from wai.annotations.core.instance import FileInfo, Instance
from wai.annotations.core.specifier import DomainSpecifier

# Define the file-info type which holds dataset item data
class MyFileInfo(FileInfo):
    @classmethod
    def from_file_data(cls, file_name: str, file_data: bytes) -> 'MyFileInfo':
        # If we don't need any additional information, or it is calculated in the init method
        return cls(file_name, file_data)
        
# Define the type of annotations for the domain
class MyAnnotations:
    ...
    
# Define an instance type with additional functionality, if required
class MyInstance(Instance[MyFileInfo, MyAnnotations]):
    def additional_method(self):
        ...

# Define the domain specifier reporting the various classes for domain instances
class MyDomainSpecifier(DomainSpecifier):
    @classmethod
    def domain_name(cls) -> str:
        return "my domain"
        
    @classmethod
    def file_type(cls) -> Type[MyFileInfo]:
        return MyFileInfo
        
    @classmethod
    def annotations_type(cls) -> Type[MyAnnotations]:
        return MyAnnotations
        
    # If our instances need additional functionality, we can override this method. The default is
    # wai.annotations.core.instance.Instance[cls.file_type(), cls.annotations_type()], and if we
    # do override this method, the type returned must inherit from this default type.
    @classmethod
    def instance_class(cls) -> Type[Instance]:
        return MyInstance
```

## Writing New Components

The base classes for components can be imported from wai-annotations' core package:

```python
from wai.annotations.core.component import Reader, InputConverter  # For input formats
from wai.annotations.core.component import InlineStreamProcessor  # For ISPs
from wai.annotations.core.component import CrossDomainConverter  # For XDCs
from wai.annotations.core.component import Writer, OutputConverter  # For output formats
```

Sub-class the base classes for the type of component you are trying to implement, and fill in the generic
type-parameters and abstract methods.

For generic type-parameters, component base classes vary on instance types, which are defined in the domain specifier
for the domains the component operates in. Therefore the best way to specify the instance type-parameter is to import
the domain specifiers for the domains of interest and use their `instance_class()` methods.

For the abstract methods, each component has a few methods which require implementation. The purpose of each should be
fairly self-explanatory, but the following examples will (hopefully) illustrate how to use each base class.

### Input Formats

Input formats consist of 2 components, a reader and an input-converter. The reader reads files from disk into an
arbitrary format, and the input-converter converts that format into the instance format for the domain of the dataset.
An example of how to implement a new input-format:

```python
from typing import Iterator, IO, Type

from wai.annotations.core.component import Reader, InputConverter
from wai.annotations.core.specifier import InputFormatSpecifier
from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier

# Get the instance type from the domain specifier
ImageObjectDetectionInstance = ImageObjectDetectionDomainSpecifier.instance_class()

# Define the external format in any way you like (if being used with an output format as well,
# define separately and import)
class MyExternalFormat:
    @classmethod
    def from_annotation_file(cls, file: IO[bytes]) -> 'MyExternalFormat':
        ...
        
    @classmethod
    def from_negative_file(cls, file: IO[bytes]) -> 'MyExternalFormat':
        ...
        
    def to_image_object_detection_instance(self) -> ImageObjectDetectionInstance:
        ...

# Define your reader, which parses files into your external format
class MyReader(Reader[MyExternalFormat]):
    # Returns an iterator of instances in the given file, in case a single file
    # contains multiple dataset items
    def read_annotation_file(self, filename: str) -> Iterator[MyExternalFormat]:
        with open(filename, "rb") as file:
            yield MyExternalFormat.from_annotation_file(file)
    
    # Returns an iterator of negative instances in the given file
    def read_negative_file(self, filename: str) -> Iterator[MyExternalFormat]:
        with open(filename, "rb") as file:
            yield MyExternalFormat.from_negative_file(file)

# Define your input converter, which converts your external format into the domain of interest (image object-detection
# in this example)
class MyInputConverter(InputConverter[MyExternalFormat, ImageObjectDetectionInstance]):
    # Converts the instance from its external format to the domain format
    def convert(self, instance: MyExternalFormat) -> Iterator[ImageObjectDetectionInstance]:
        yield instance.to_image_object_detection_instance()
        
# Create a specifier to advertise our input format to the plugin system
class MyInputFormatSpecifier(InputFormatSpecifier):
    # The domain of the input format
    @classmethod
    def domain(cls) -> Type[ImageObjectDetectionDomainSpecifier]:
        return ImageObjectDetectionDomainSpecifier
    
    # The reader class we defined earlier
    @classmethod
    def reader(cls) -> Type[MyReader]:
        return MyReader
    
    # The input converter class we defined earlier
    @classmethod
    def input_converter(cls) -> Type[MyInputConverter]:
        return MyInputConverter
```

### Inline Stream Processors

```python
from typing import Iterable, Optional, Set, Type

from wai.annotations.core.component import InlineStreamProcessor
from wai.annotations.core.specifier import ISPSpecifier, DomainSpecifier
from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier

# Get the instance type from the domain specifier
ImageObjectDetectionInstance = ImageObjectDetectionDomainSpecifier.instance_class()

# Define the ISP
class MyISP(InlineStreamProcessor[ImageObjectDetectionInstance]):
    # Takes an instance from the conversion stream and processes it. Returns an iterable so that new
    # instances can be injected into the conversion stream, or removed from it
    def _process_element(self, element: ImageObjectDetectionInstance) -> Iterable[ImageObjectDetectionInstance]:
        ...
        
# Advertise the ISP to the plugin system via a specifier
class MyISPSpecifier(ISPSpecifier):
    # Specifies the domains this ISP can operate on. None indicates any domain, and a set indicates
    # a set of specific domains
    @classmethod
    def domains(cls) -> Optional[Set[Type[DomainSpecifier]]]:
        return {ImageObjectDetectionDomainSpecifier}
        
    # The actual ISP type we defined earlier
    @classmethod
    def processor_type(cls) -> Type[InlineStreamProcessor]:
        return MyISP
```

### Cross-Domain Converters

```python
from typing import Iterable, Type

from wai.annotations.core.component import CrossDomainConverter
from wai.annotations.core.specifier import XDCSpecifier, DomainSpecifier
from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier

# Get the instance types from the domain specifiers
ImageClassificationInstance = ImageClassificationDomainSpecifier.instance_class()
ImageObjectDetectionInstance = ImageObjectDetectionDomainSpecifier.instance_class()

# Define your XDC, in this case converting from the image object-detection domain to
# the image classification domain
class MyXDC(CrossDomainConverter[ImageObjectDetectionInstance, ImageClassificationInstance]):
    # Convert the instance, returning an iterable again to allow insertion/deletion of instances
    def _convert_element(self, element: ImageObjectDetectionInstance) -> Iterable[ImageClassificationInstance]:
        ...

# Define the specifier to advertise our new XDC to the plugin system
class MyXDCSpecifier(XDCSpecifier):
    # Declare the input domain of the converter
    @classmethod
    def from_domain(cls) -> Type[DomainSpecifier]:
        return ImageObjectDetectionDomainSpecifier
    
    # Declare the output domain of the converter
    @classmethod
    def to_domain(cls) -> Type[DomainSpecifier]:
        return ImageClassificationDomainSpecifier
    
    # Advertise our XDC defined earlier
    @classmethod
    def converter(cls) -> Type[CrossDomainConverter]:
        return MyXDC
```

### Output Formats

Output formats also consist of 2 components, a writer and an output-converter. The output-converter converts instances
from the domain format to an arbitrary external format for the output format, and the writer writes the instances in
that format to disk. An example of how to implement a new output-format:

```python
from typing import Iterator, IO, Type, Iterable

from wai.annotations.core.component import Writer, OutputConverter
from wai.annotations.core.instance import FileInfo
from wai.annotations.core.specifier import OutputFormatSpecifier, DomainSpecifier
from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier

# Get the instance type from the domain specifier
ImageObjectDetectionInstance = ImageObjectDetectionDomainSpecifier.instance_class()

# Define the external format in any way you like (if being used with an input format as well, define
# separately and import)
class MyExternalFormat:
    @classmethod
    def from_image_object_detection_instance(cls, instance: ImageObjectDetectionInstance) -> 'MyExternalFormat':
        ...

# Define your writer, which writes instances of your external format to disk
class MyWriter(Writer[MyExternalFormat]):
    # Depending on the external format, it might write all instances to a single file,
    # or each instance to its own file in a directory. Provide some helpful information
    # on which is the case here 
    @classmethod
    def output_help_text(cls) -> str:
        ...
    
    # How to write the actual instances to disk
    def write(self, instances: Iterable[MyExternalFormat], path: str):
        ...
    
    # Whether the output option should be a file (if not, then it should be
    # a directory)
    def expects_file(self) -> bool:
        ...
    
    # Lets wai-annotations extract the file from your external format
    def extract_file_info_from_external_format(self, instance: MyExternalFormat) -> FileInfo:
        ...

# Define your output converter, which converts instances from the format's domain (image object-detection
# in this example) into your external format
class MyOutputConverter(OutputConverter[ImageObjectDetectionInstance, MyExternalFormat]):
    # Converts the instance from the domain format into your external format
    def convert(self, instance: ImageObjectDetectionInstance) -> Iterator[MyExternalFormat]:
        yield MyExternalFormat.from_image_object_detection_instance(instance)
        
# Create a specifier to advertise our output format to the plugin system
class MyOutputFormatSpecifier(OutputFormatSpecifier):
    # Specify the domain the format is in
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        return ImageObjectDetectionDomainSpecifier
    # Specify the writer we declared earlier
    @classmethod
    def writer(cls) -> Type[Writer]:
        return MyWriter
    
    # Specify the output converter we declared earlier
    @classmethod
    def output_converter(cls) -> Type[OutputConverter]:
        return MyOutputConverter
```

### Best Practice

Although in each of the examples shown here, we have defined our plugin specifiers in the same file as the components
they advertise, this is not the recommended approach. The specifier types should instead be defined in their own
sub-package, and the methods should locally import the specified types (instead of globally at the beginning of the
specifier Python file). This is so the specifier can be imported into the plugin system without importing potentially
heavy-weight libraries that the components depend on for their functionality. This way the system can provide reflection
of the available plugins, but only load those plugins that are actually selected for use in a conversion.

## Advertising Plugins

In order for wai-annotations to recognise your plugin, the specified needs to be advertised as an entry point in your
setup script under the `wai.annotations.plugins` group:

```python
# setup.py
from setuptools import setup

setup(
    ...,
    entry_points={
        "wai.annotations.plugins": [
            # Input Formats
            "from-my-input-format=com.example.specifiers:MyInputFormatSpecifier",
            
            # Output Formats
            "to-my-output-format=com.example.specifiers:MyOutputFormatSpecifier",

            # ISPs
            "my-isp=com.example.specifiers:MyISPSpecifier",

            # XDCs
            "my-xdc=com.example.specifiers:MyXDCSpecifier"
        ]
    }
)

```

## Adding Command-Line Options to Plugin Components

TODO
