from setuptools import setup, find_packages

setup(
    name="plpd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.26.4",
        "pandas>=2.2.3",
        "scikit-learn>=1.1.3",
        "Pillow>=10.4.0",
        "matplotlib>=3.6.2",
        "missingno>=0.5.2",
        "xgboost>=2.1.2"
    ],
)