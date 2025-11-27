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
    python_requires=">=3.8",
)
