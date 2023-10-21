# -*- coding: utf-8 -*-

import setuptools
import pathlib


HERE = pathlib.Path(__file__).parent

# The text of the README file
long_description = (HERE / "README.md").read_text()

setuptools.setup(
    name='pyspacemouse',
    version='1.1.0',
    author='Jakub Andrýsek',
    author_email='email@kubaandrysek.cz',
    description='Multiplatform Python interface to the 3DConnexion Space Mouse - forked from pyspacenavigator',
    url='https://github.com/JakubAndrysek/pyspacemouse',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='pyspacemouse, 3d, 6 DoF, HID, python, open-source, spacemouse, spacenavigator, 3dconnection, 3d-mouse',
    license='MIT',
    packages=['pyspacemouse'],
    install_requires=[
        "easyhid",
    ],
    extras_require={
        'develop': [
            'mkdocs',
            'mkdocs-material',
            'mkdocs-glightbox',
            'mkdocs-redirects',
            'mkdoxy',
            'mkdocs-open-in-new-tab',
            'mkdocs-git-revision-date-localized-plugin'],
    },

    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.8",
)
