from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.3'
DESCRIPTION = 'Python module for Spectral BLDC motor controllers'

# Setting up
setup(
    name="SourceRoboticsToolbox",
    version=VERSION,
    author="Source robotics (Petar Crnjak)",
    author_email="<info@source-robotics.com>",
    license = "MIT",
    project_urls = {
        "Documentation": "https://github.com/PCrnjak/Source-Robotics-Toolbox",
        "Source": "https://github.com/PCrnjak/Source-Robotics-Toolbox",
    },
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.10",
    keywords=['python', 'BLDC', 'CANBUS', 'Robot', 'Source robotics', 'robotics'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)