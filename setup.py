from setuptools import setup, find_packages

setup(
    name="custompackage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here

    description="A custom Python package for testing AWS CodeArtifact",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RuchiSagar002655548/cy-RTD/tree/main/custompackage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
