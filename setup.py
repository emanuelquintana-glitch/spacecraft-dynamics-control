from setuptools import setup, find_packages

setup(
    name="spacecraft-dynamics-control",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0",
        "plotly>=5.0.0",
    ],
    author="Emanuel Quintana",
    author_email="emanuel.quintana@example.com",
    description="Educational material on spacecraft dynamics and control",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emanuelquintana/spacecraft-dynamics-control",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    keywords=["spacecraft", "dynamics", "control", "aerospace", "education"],
)
