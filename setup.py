from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="melodymover",
    version="1.0.0",
    author="Cristian Novoa",
    author_email="cnovoa.o@gmail.com",
    description="A powerful and user-friendly desktop application for organizing and managing music collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cristian158/melodymover",
    packages=find_packages(include=['melodymover', 'melodymover.*']),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyGObject",
        "mutagen",
    ],
    entry_points={
        "console_scripts": [
            "melodymover=melodymover.MelodyMover:main",
        ],
    },
    package_data={
        "melodymover": ["*.glade"],
    },
    include_package_data=True,
    license="MIT",
    platforms=["any"],
)
