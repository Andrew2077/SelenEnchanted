import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(this_dir, "requirements.txt")


with open(requirements_path) as f:
    required = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="selen-enchanted",
    version="0.0.10.3",
    packages=find_packages(),
    author="Andrew Naaem",
    author_email="andrew.naaem99@gmail.com",
    license="Apache License 2.0",
    install_requires=required,
    description="A selenium wrapper that makes it easier to use",
    url="https://github.com/Andrew2077/SelenEnchanted",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords=["selenium", "wrapper", "automation", "testing"],
)
