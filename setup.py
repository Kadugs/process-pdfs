from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="process-pdfs",
    version="0.1.0",
    description=(
        "A small ETL pipeline that extracts "
        "structured information from PDF files"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carlos Eduardo Gomes Silva",
    author_email="66494905+Kadugs@users.noreply.github.com",
    python_requires=">=3.12",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pdfplumber>=0.11.7",
        "matplotlib>=3.7.1",
        "pandas>=2.0.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "process-pdfs=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    keywords="pdf processing etl data-extraction document-processing",
    project_urls={
        "Bug Reports": "https://github.com/Kadugs/process-pdfs/issues",
        "Source": "https://github.com/Kadugs/process-pdfs",
    },
)
