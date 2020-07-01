# How to Use Wai-Annotations from the Command-Line

To convert a dataset using wai-annotations from the command-line, run the following command:

```
convert-annotations [GLOBAL OPTIONS] \
    input-type [INPUT OPTIONS] \
    [ISP/XDC [ISP/XDC OPTIONS]]... \
    output-type [OUTPUT OPTIONS]
```

For the available global options, see [here](GLOBAL_OPTIONS.md).

For all other options, run:

```
convert-annotations --list-plugins
```

for the list of available plugins in your environment and how to use them.

Examples of how to run wai-annotations can be found [here](EXAMPLES.md).
