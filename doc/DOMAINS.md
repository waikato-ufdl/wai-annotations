# Builtin Domains in Wai-Annotations

wai-annotations currently comes with 2 built-in domains: image object-detection and image classification. More domains
are planned for the future, and this document will be updated with those as they are introduced.

## Image Object-Detection

This domain pertains to finding regions of still images which contain identifiable objects, and was the original scope
of wai-annotations. Instances in this domain contain an image as the dataset item and a set of labelled regions (either
axis-aligned boxes or segmented polygons) identifying the detected objects.

## Image Classification

This domain deals with labelling entire images as containing a certain subject. Instances in this domain contain an
image and a string label classifying the image.
