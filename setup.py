from setuptools import setup, find_packages

setup(
    name="bunnycdnpython",
    version="0.0.1",
    author="mathrithms",
    author_email="hello@mathrithms.com",
    description="A python SDK for BunnyCDN",
    url="https://github.com/mathrithms/BunnyCDN-Python-Lib.git",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
