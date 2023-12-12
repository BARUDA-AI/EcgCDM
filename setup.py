from setuptools import setup, find_packages

setup(
    name='ecgcdm',
    version='0.1.0',
    packages=find_packages(include=['preprocess.preprocess_snuh_ecg', 'mk_cdm']),
    install_requires=[
        'pandas',
        'numpy',
    ],
    extras_require={
        'interactive': ['matplotlib>=2.2.0', 'jupyter'],
    }
)