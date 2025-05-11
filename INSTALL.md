# Installation Guide

## Option 1: Using pip (if you have a compatible C++ compiler)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Option 2: Using conda (recommended for Windows users)

This is the recommended approach for Windows users who are experiencing build errors with pip.

1. First, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/individual)

2. Create and activate the conda environment:

```bash
# Create the environment from the environment.yml file
conda env create -f environment.yml

# Activate the environment
conda activate agri-yield
```

## Running the Application

After installing the dependencies using either method:

```bash
# Run the application
python run.py
```

The application will be available at http://localhost:8000

You can access the API documentation at http://localhost:8000/docs 