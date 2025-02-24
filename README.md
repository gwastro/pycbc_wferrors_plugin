# pycbc_wferrors_plugin

Plugin for PyCBC to apply systematic errors models to gravitational waveforms.
To see how it can be used, please refer to the [examples](examples) folder. It
contains a folder [notebooks](example/notebooks) which contains an example notebook.
Another folder [config_files](example/config_files) contains the example configuration 
files for the PE runs with PyCBC Inference. 

## Installation

It can be installed by running either one of
```bash
pip install git+https://github.com/gwastro/example-waveform-plugin.git
```
or, using an SSH key pair,
```bash
pip install git+ssh://git@github.com/gwastro/example-waveform-plugin.git
```
Alternatively, clone this repository, navigate to the corresponding folder and run
```bash
pip install .
```

## Code Plans

Besides updating the documentation, we plan to provide a generator for time
domain waveforms soon.

Moreover, work is in progress to provide the same functionality for the
LAL waveforms interface `gwsignal`.
