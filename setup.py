from setuptools import setup, find_namespace_packages


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
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai"
    ],
    version="0.3.2",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "wai.common>=0.0.28,<=0.0.30",
        "wai.json>=0.0.4,<0.1",
        "wai.bynning>=0.0.1,<0.1",
        "Cython",
        "Pillow",
        "contextlib2",
        "numpy",
        "planar",
        "scikit-image",
        "pycocotools",
        "opencv-python",
    ],
    entry_points={
        "console_scripts": ["convert-annotations=wai.annotations.main:sys_main"],
        "wai.annotations.formats": ["adams=wai.annotations.adams:ADAMSFormatSpecifier",
                                    "coco=wai.annotations.coco:COCOFormatSpecifier",
                                    "roi=wai.annotations.roi:ROIFormatSpecifier",
                                    "tfrecords=wai.annotations.tf:TFFormatSpecifier",
                                    "vgg=wai.annotations.vgg:VGGFormatSpecifier"]
    }
)
