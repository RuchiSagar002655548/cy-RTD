from setuptools import setup, find_packages

setup(
    name="custom_py_package",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here

    description="A custom Python package for testing AWS CodeArtifact",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RuchiSagar002655548/cy-RTD/tree/main/custom_py_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
