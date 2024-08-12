"""
To install run 
```
python setup.py sdist bdist_wheel
twine check dist/*
```
it should return
```
Checking dist\selen_enchanted-0.0.10-py3-none-any.whl: PASSED
Checking dist\selen_enchanted-0.1-py3-none-any.whl: PASSED
Checking dist\selen_enchanted-0.0.10.tar.gz: PASSED
Checking dist\selen_enchanted-0.1.tar.gz: PASSED
```
"""

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

requirements = [
    "chromedriver_autoinstaller==0.6.2",
    "requests==2.32.3",
    "selenium==4.23.1",
    "selenium_wire==5.1.0",
    "ua_generator==0.5.1",
    "user_agents==2.2.0",
    "webdriver_manager==4.0.1"
]


setup(
    name='selen-enchanted',
    version='0.0.10.0',
    packages=find_packages(),
    author="Andrew Naaem",
    author_email="andrew.naaem99@gmail.com",
    license='Apache License 2.0',
    install_requires=requirements,
    description='A selenium wrapper that makes it easier to use',
    url="https://github.com/Andrew2077/SelenEnchanted",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords=['selenium', 'wrapper', 'automation', 'testing'],
)