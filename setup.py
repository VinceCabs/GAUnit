import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gaunit",
    version="0.0.1",
    author="Vincent Cabanis",
    author_email="touch@cabanis.fr",
    description="Testing Google Analytics implementations within CI pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VinceCabs/GAUnit",
    packages=["gaunit"],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.6",
)
