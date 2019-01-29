from setuptools import setup, find_packages

setup(
    name="splitter",
    version="0.1.0",
    install_requires=[
        "click",
    ],
    author="Laura Bostan",
    author_email="sarnthil@gmail.com",
    description="Split datasets into train/dev/test/etc.",
    url="https://github.com/sarnthil/splitter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
    entry_points={
        "console_scripts": ["splitter=splitter:cli"],
    },
)
