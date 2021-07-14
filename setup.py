from setuptools import setup, find_packages


def readall(path):
    with open(path) as fp:
        return fp.read()


setup(
    name="bunnycdnpython",
    version="0.0.7",
    author="mathrithms",
    author_email="hello@mathrithms.com",
    description="A python SDK for BunnyCDN",
    long_description=readall("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mathrithms/BunnyCDN-Python-Lib",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
