import io
import os

import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))

ABOUT = {}
with io.open(os.path.join(HERE, "gaunit", "__about__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), ABOUT)
with io.open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()


setuptools.setup(
    name="gaunit",
    version=ABOUT["__version__"],
    author="Vincent Cabanis",
    author_email="touch@cabanis.fr",
    description="Testing Google Analytics implementations within CI pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VinceCabs/GAUnit",
    packages=["gaunit"],
    package_data={"gaunit": ["config.json"]},
    entry_points={"console_scripts": ["gaunit=gaunit.cli:main"]},
    license="MIT",
    python_requires=">=3.6",
    install_requires=["colorama==0.4.4"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
    ],
)
