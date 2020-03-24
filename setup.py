import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="photodl",
    version="0.1.0",
    author="8F3E",
    description="A simple python package to download, sort and backup photos "
                "from an SD card.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/8F3E/photodl",
    packages=setuptools.find_packages(),
    install_requires=[
        "exif"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
