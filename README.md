# pycbc_wferrors_plugin

Plugin for PyCBC to incorporate systematic errors in gravitational waveforms models.
This plugin can be used with any waveform model which can be called with 
[pycbc-waveform](https://pycbc.org/pycbc/latest/html/waveform.html) 
module. There are two waveform error parametrizations: one uses absolute errors in 
phase, while the other uses relative errors in phase. Both parametrization uses relative errors
in Amplitude. The description of these parametrizations can be found in the companion paper: [arXiv:2502.17400](https://arxiv.org/abs/2502.17400)


To see how it can be used, please refer to the [examples](examples) folder. It
contains a folder [notebooks](examples/notebooks) which contains an example notebook.
Another folder [config_files](examples/config_files) contains the example configuration 
files for the PE runs with PyCBC Inference. 

## Installation
To see example of PyCBC waveform plugin, you can refer to [PyCBC Inference #9](https://github.com/gwastro/PyCBC-Tutorials/blob/master/tutorial/inference_9_AddingCustomModels.ipynb)
in [PyCBC Tutorials repository](https://github.com/gwastro/PyCBC-Tutorials/tree/master).

The WF-Error plugin can be installed by running either one of
```bash
pip install git+https://github.com/gwastro/pycbc_wferrors_plugin.git
```
or, using an SSH key pair,
```bash
pip install git+ssh://git@github.com/gwastro/pycbc_wferrors_plugin.git
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
