# -*- coding: utf-8 -*-

import setuptools
import pathlib


HERE = pathlib.Path(__file__).parent

# The text of the README file
long_description = (HERE / "README.md").read_text()

setuptools.setup(
    name='pyspacemouse',
    version='1.0.1',
    author='Jakub Andrýsek',
    author_email='email@kubaandrysek.cz',
    description='Multiplatform Python interface to the 3DConnexion Space Mouse - forked from pyspacenavigator',
    url='https://github.com/JakubAndrysek/pyspacemouse',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='pyspacemouse, 3d, 6 DoF, HID',
    license='MIT',
    packages=['pyspacemouse'],
    install_requires=[
        "easyhid",
        "typing",
    ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
