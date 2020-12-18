# Domains
## Image Classification Domain
Images categorised by content.

The image classification domain deals with labelling entire images as containing a certain subject. Instances in this
domain contain an image and a string label classifying the image.


## Image Object-Detection Domain
Images containing multiple identified objects.

The image object-detection domain pertains to finding regions of still images which contain identifiable objects.
Instances in this domain consist of an image and a set of regions (either axis-aligned boxes or polygons), each with
an accompanying label, identifying the detected objects within the image.


## Image Segmentation Domain
Images segmented by category.

The image segmentation domain 'colourises' an image by assigning a category to each pixel (where no category
corresponds to 'the background'). Instances in this domain are a still image and a corresponding table of the same
size, where each element is a label.


## Speech Domain
Transcriptions of recorded speech.

The speech domain covers audio data of people speaking natural languages, annotated with text transcribing the verbal
contents of the audio. Instances in this domain are an audio file and a string containing the transcription.


