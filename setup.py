import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grump",
    version="0.0.5",
    author="Andrew Solomon",
    author_email="andrew@geekuni.com",
    description="Grep for Unstructured Multiline Paragraphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewsolomon/grump",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "grump=grump.grump:main"
        ],
    }
)
