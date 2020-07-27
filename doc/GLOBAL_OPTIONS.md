# Global Options for Wai-Annotations

The following options can be specified before any stages in the conversion chain, and globally affect the process of
converting datasets:

* `-v`, `--verbosity`: Optional argument to set the logging verbosity of the conversion. Can be
                       specified multiple times to further increase verbosity.

* `--list-plugins`: If provided, lists all of the plugins registered with wai-annotations, and then
                    quits.

* `--debug`: If provided, processing stages will buffer their conversions, allowing for easier debugging
             in an interactive debugger (can see the results of conversions at the stages where they happen).
