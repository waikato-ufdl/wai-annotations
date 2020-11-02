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
    version="0.5.3",
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
            # Image Object Detection Formats
            "from-adams-od=wai.annotations.format.adams.od.specifier:ADAMSODInputFormatSpecifier",
            "to-adams-od=wai.annotations.format.adams.od.specifier:ADAMSODOutputFormatSpecifier",
            "from-coco-od=wai.annotations.format.coco.specifier:COCOInputFormatSpecifier",
            "to-coco-od=wai.annotations.format.coco.specifier:COCOOutputFormatSpecifier",
            "from-roi-od=wai.annotations.format.roi.specifier:ROIInputFormatSpecifier",
            "to-roi-od=wai.annotations.format.roi.specifier:ROIOutputFormatSpecifier",
            "from-tf-od=wai.annotations.format.tf.specifier:TFRecordsInputFormatSpecifier",
            "to-tf-od=wai.annotations.format.tf.specifier:TFRecordsOutputFormatSpecifier",
            "from-vgg-od=wai.annotations.format.vgg.specifier:VGGInputFormatSpecifier",
            "to-vgg-od=wai.annotations.format.vgg.specifier:VGGOutputFormatSpecifier",

            # Image Classification Formats
            "from-adams-ic=wai.annotations.format.adams.ic.specifier:ADAMSICInputFormatSpecifier",
            "to-adams-ic=wai.annotations.format.adams.ic.specifier:ADAMSICOutputFormatSpecifier",
            "from-subdir-ic=wai.annotations.format.subdir.specifier:SubDirInputFormatSpecifier",
            "to-subdir-ic=wai.annotations.format.subdir.specifier:SubDirOutputFormatSpecifier",

            # Image Segmentation Formats
            "from-blue-channel-is=wai.annotations.format.blue_channel.specifier:BlueChannelInputFormatSpecifier",
            "to-blue-channel-is=wai.annotations.format.blue_channel.specifier:BlueChannelOutputFormatSpecifier",
            "from-indexed-png-is=wai.annotations.format.indexed_png.specifier:IndexedPNGInputFormatSpecifier",
            "to-indexed-png-is=wai.annotations.format.indexed_png.specifier:IndexedPNGOutputFormatSpecifier",
            "from-layer-segments-is=wai.annotations.format.layer_segments.specifier:LayerSegmentsSourceStageSpecifier",
            "to-layer-segments-is=wai.annotations.format.layer_segments.specifier:LayerSegmentsSinkStageSpecifier",

            # Speech Formats
            "from-common-voice-sp=wai.annotations.format.common_voice.specifier:CommonVoiceInputFormatSpecifier",
            "to-common-voice-sp=wai.annotations.format.common_voice.specifier:CommonVoiceOutputFormatSpecifier",
            "from-festvox-sp=wai.annotations.format.festvox.specifier:FestVoxInputFormatSpecifier",
            "to-festvox-sp=wai.annotations.format.festvox.specifier:FestVoxOutputFormatSpecifier",

            # ISPs
            "coerce-box=wai.annotations.isp.coercions.specifier:BoxBoundsCoercionISPSpecifier",
            "coerce-mask=wai.annotations.isp.coercions.specifier:MaskBoundsCoercionISPSpecifier",
            "convert-image-format=wai.annotations.isp.convert_image_format.specifier:ConvertImageFormatISPSpecifier",
            "dimension-discarder=wai.annotations.isp.dimension_discarder.specifier:DimensionDiscarderISPSpecifier",
            "discard-negatives=wai.annotations.isp.discard_negatives.specifier:DiscardNegativesISPSpecifier",
            "check-duplicate-filenames=wai.annotations.isp.duplicate_filenames.specifier:DuplicateFileNamesISPSpecifier",
            "filter-labels=wai.annotations.isp.filter_labels.specifier:FilterLabelsISPSpecifier",
            "map-labels=wai.annotations.isp.map_labels.specifier:MapLabelsISPSpecifier",
            "passthrough=wai.annotations.isp.passthrough.specifier:PassThroughISPSpecifier",
            "remove-classes=wai.annotations.isp.remove_classes.specifier:RemoveClassesISPSpecifier",
            "strip-annotations=wai.annotations.isp.strip_annotations.specifier:StripAnnotationsISPSpecifier",

            # XDCs
            "od-to-is=wai.annotations.xdc.od_to_is.specifier:OD2ISXDCSpecifier",
        ]
    }
)
