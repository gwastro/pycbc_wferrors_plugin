
"""
setup.py file for waveform-errors from pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command
from setuptools import find_packages


setup (
    name = 'pycbc-wferrors_test',
    description = 'An example waveform plugin for PyCBC',
    long_description = open('descr.rst').read(),
    author = 'The PyCBC team',
    author_email = 'sumit.kumar@aei.mpg.de',
    url = 'http://www.pycbc.org/',
    keywords = ['pycbc', 'signal processing', 'gravitational waves'],
    install_requires = ['pycbc'],
    py_modules = ['wferrors'],
    entry_points = {"pycbc.waveform.fd":"wferrors = wferrors:amplitude_phase_modification_fd"},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
