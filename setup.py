from setuptools import setup, find_packages

setup(
    name="scoutpulse-core",
    version="0.2.0",
    description="Enterprise Autonomous GitHub Discovery & Sybil Star-Gaming Defense Engine",
    author="Aamir Zameer",
    author_email="aamir@amz34.com",
    url="https://github.com/Amz34/scout-pulse-core",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "scoutpulse=scoutpulse.cli.main:main",
        ],
    },
)
