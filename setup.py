from setuptools import setup

exec(open("skunk/version.py").read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="skunk",
    version=__version__,
    description="Insert SVGs into matplotlib figures",
    author="Andrew White",
    author_email="white.d.andrew@gmail.com",
    url="https://github.com/whitead/skunk",
    license="MIT",
    packages=["skunk"],
    install_requires=["matplotlib"],
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Matplotlib",
    ],
)
