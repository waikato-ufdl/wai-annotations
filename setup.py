from setuptools import setup


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations",
    description="Python library for converting image and object annotations formats into each other.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-datamining/wai-annotations",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    version="0.7.8",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "wai.annotations.core>=0.1.8",
        "wai.annotations.adams>=1.0.1",
        "wai.annotations.audio>=1.0.1",
        "wai.annotations.bluechannel>=1.0.2",
        "wai.annotations.coco>=1.0.2",
        "wai.annotations.commonvoice>=1.0.2",
        "wai.annotations.festvox>=1.0.0",
        "wai.annotations.generic>=1.0.0",
        "wai.annotations.grayscale>=1.0.1",
        "wai.annotations.imgaug>=1.0.6",
        "wai.annotations.imgstats>=1.0.3",
        "wai.annotations.imgvis>=1.0.3",
        "wai.annotations.indexedpng>=1.0.1",
        "wai.annotations.layersegments>=1.0.2",
        "wai.annotations.opex>=1.0.0",
        "wai.annotations.redis.predictions>=1.0.2",
        "wai.annotations.roi>=1.0.1",
        "wai.annotations.subdir>=1.0.1",
        "wai.annotations.vgg>=1.0.0",
        "wai.annotations.video>=1.0.2",
        "wai.annotations.voc>=1.1.0",
        "wai.annotations.yolo>=1.0.1"
    ],
    extras_require={
        "tf": ["wai.annotations.tf>=1.3.0"],
    },
)
