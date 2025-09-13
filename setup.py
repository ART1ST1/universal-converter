#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read requirements
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read README if it exists
long_description = "Universal Converter - A powerful desktop application for converting files between various formats"
if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="universal-converter",
    version="1.0.0",
    description="Universal file format converter with modern GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Universal Converter Team",
    author_email="contact@universalconverter.com",
    url="https://github.com/universalconverter/universal-converter",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-qt>=4.0',
            'black>=21.0',
            'flake8>=3.8'
        ]
    },
    entry_points={
        'console_scripts': [
            'universal-converter=main:main',
        ],
        'gui_scripts': [
            'universal-converter-gui=main:main',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Utilities"
    ],
    python_requires=">=3.8",
    keywords="converter, file format, image, video, audio, document, pdf",
    project_urls={
        "Bug Reports": "https://github.com/universalconverter/universal-converter/issues",
        "Source": "https://github.com/universalconverter/universal-converter",
        "Documentation": "https://github.com/universalconverter/universal-converter/wiki"
    }
)