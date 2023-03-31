"""Project installation script."""

from setuptools import find_namespace_packages, setup

setup(
    name="ansys-scade-apitools",
    version="0.1.dev0",
    url="https://github.com/ansys-scade/apitools",
    author="ANSYS, Inc.",
    author_email="scade-support@ansys.com",
    maintainer="ANSYS, Inc.",
    maintainer_email="scade-support@ansys.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    license="MIT",
    license_file="LICENSE",
    description="An extension library for SCADE Python APIs",
    long_description=open("README.rst").read(),
    install_requires=[
        "importlib-metadata >= 1.0; python_version < '3.8'",
        "importlib-metadata >= 4.0; python_version >= '3.8'",
    ],
    keywords=["scade", "git", "merge"],
    # only 3.4 and 3.7. 3.10 in a near future, with 2023 R2
    python_requires=">=3.4, !=3.5.*, !=3.6.*, !=3.8.*, !=3.9.*, <3.11",
    packages=find_namespace_packages(where="src", include="ansys*"),
    package_dir={"": "src"},
)
