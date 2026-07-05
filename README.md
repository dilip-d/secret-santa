# Secret Santa Assignment System

A modular Python application that automates Secret Santa gift assignments while ensuring:
- No employee is assigned to themselves.
- Each employee is assigned exactly one secret child.
- Previous year's assignments can be avoided.
- Results are exported to a CSV file.

## Features

- Automatic Secret Santa assignment generation
- CSV input and output
- Support for previous year's assignments
- Validation for invalid or duplicate employee data
- Modular architecture
- Unit tests
- Error handling

## Prerequisites

- Python 3.8 or later
- pip

## Installation

```bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
pip install -r requirements.txt
```

## Usage

Without previous assignments:

```bash
python run.py data/employees.csv
```

With previous assignments:

```bash
python run.py data/employees.csv --previous data/previous_assignments.csv
```

The generated assignments will be written to:

```
output/secret_santa_assignments.csv
```