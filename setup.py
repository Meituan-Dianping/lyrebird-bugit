import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lyrebird-bugit',
    version='1.9.0',
    packages=['lyrebird_bugit'],
    url='https://github.com/Meituan-Dianping/lyrebird-bugit',
    author='HBQA',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ),
    entry_points={
        'lyrebird_plugin': [
            'bugit = lyrebird_bugit.manifest'
        ]
    },
    install_requires=[
        "lyrebird"
    ])
