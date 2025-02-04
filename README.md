# signac_metadata
Parse metadata stored in JSON file.

## Authors

S. Stoica

University of Groningen


## Description

This repository contains code to extract and attach metadata of  Molecular Dynamics simulations managed by signac. 

The data is stored in iRODS into folders for each simulation with each folder containing the simulation parameters (metadata) as a JSON file named signac_statepoint.json.

## Requirements 

- Python 3 ( >=3.8)
- python-irodsclient

## Virtual environment
```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## run 

```
python parse_metadata.py
```
