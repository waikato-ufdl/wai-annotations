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
    version="0.4.6",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "wai.common>=0.0.35",
        "wai.json>=0.0.4,<0.1",
        "wai.bynning>=0.0.2,<0.1",
        "Cython",
        "Pillow",
        "contextlib2",
        "numpy>=1.16,<=1.17.4",
        "planar",
        "scikit-image",
        "wai.pycocotools",
        "opencv-python",
    ],
    entry_points={
        "console_scripts": ["convert-annotations=wai.annotations.main:sys_main"],
        "wai.annotations.plugins": [
            # Formats
            "from-adams-od=wai.annotations.format.specifiers:ADAMSODInputFormatSpecifier",
            "to-adams-od=wai.annotations.format.specifiers:ADAMSODOutputFormatSpecifier",
            "from-adams-ic=wai.annotations.format.specifiers:ADAMSICInputFormatSpecifier",
            "to-adams-ic=wai.annotations.format.specifiers:ADAMSICOutputFormatSpecifier",
            "from-coco=wai.annotations.format.specifiers:COCOInputFormatSpecifier",
            "to-coco=wai.annotations.format.specifiers:COCOOutputFormatSpecifier",
            "from-common-voice=wai.annotations.format.specifiers:CommonVoiceInputFormatSpecifier",
            "to-common-voice=wai.annotations.format.specifiers:CommonVoiceOutputFormatSpecifier",
            "from-festvox=wai.annotations.format.specifiers:FestVoxInputFormatSpecifier",
            "to-festvox=wai.annotations.format.specifiers:FestVoxOutputFormatSpecifier",
            "from-roi=wai.annotations.format.specifiers:ROIInputFormatSpecifier",
            "to-roi=wai.annotations.format.specifiers:ROIOutputFormatSpecifier",
            "from-subdir=wai.annotations.format.specifiers:SubDirInputFormatSpecifier",
            "to-subdir=wai.annotations.format.specifiers:SubDirOutputFormatSpecifier",
            "from-tfrecords=wai.annotations.format.specifiers:TFRecordsInputFormatSpecifier",
            "to-tfrecords=wai.annotations.format.specifiers:TFRecordsOutputFormatSpecifier",
            "from-vgg=wai.annotations.format.specifiers:VGGInputFormatSpecifier",
            "to-vgg=wai.annotations.format.specifiers:VGGOutputFormatSpecifier",

            # ISPs
            "coerce-box=wai.annotations.isp.specifiers:BoxBoundsCoercionISPSpecifier",
            "coerce-mask=wai.annotations.isp.specifiers:MaskBoundsCoercionISPSpecifier",
            "convert-image-format=wai.annotations.isp.specifiers:ConvertImageFormatISPSpecifier",
            "dimension-discarder=wai.annotations.isp.specifiers:DimensionDiscarderISPSpecifier",
            "discard-negatives=wai.annotations.isp.specifiers:DiscardNegativesISPSpecifier",
            "check-duplicate-filenames=wai.annotations.isp.specifiers:DuplicateFileNamesISPSpecifier",
            "filter-labels=wai.annotations.isp.specifiers:FilterLabelsISPSpecifier",
            "map-labels=wai.annotations.isp.specifiers:MapLabelsISPSpecifier",
            "passthrough=wai.annotations.isp.specifiers:PassThroughISPSpecifier",

            # XDCs
            # Currently none
        ]
    }
)
