"""
setup.py file for waveform-errors from pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command
from setuptools import find_packages

version_config = {
    'version_file': '_pycbc_wferrors_version.py',
    'version_scheme': 'no-guess-dev',
    'local_scheme': 'dirty-tag',
    'fallback_version': '0.1.0',
}


setup(
    name='pycbc-wferrors',
    use_scm_version=version_config,
    description='An waveform plugin for systematic errors for PyCBC',
    long_description=open('descr.rst').read(),
    author='The PyCBC team',
    author_email='sumit.kumar@aei.mpg.de',
    url='http://www.pycbc.org/',
    keywords=['pycbc', 'signal processing', 'gravitational waves'],
    setup_requires=[
        'setuptools>=64',
        'setuptools_scm>=8',
        'wheel',
    ],
    install_requires=['pycbc'],
    py_modules=['wferrors'],
    entry_points={
        "pycbc.waveform.fd": [
            "wferrors = wferrors:amplitude_phase_modification_fd",
            "wferrors_2p = wferrors:amplitude_phase_modification_both_polarization_fd",
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    extras_require={
        "dev": [
            # -- Documentation
            'sphinx',
            'sphinx-rtd-theme',
            'm2r2',  # Advantage: nbsphinx wants same mistune version
            'docutils>=0.18.1,<0.21',  # Prevent bug in m2r2
            # "sphinx_mdinclude",  # Either this or m2r2, not both. have different compatibility
            'nbsphinx',
            'nbsphinx-link',
            'lxml_html_clean',  # Needed by nbsphinx
        ],
    },
)
