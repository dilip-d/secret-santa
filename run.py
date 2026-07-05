#!/usr/bin/env python
"""Simple runner for Secret Santa application."""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main, parse_arguments


if __name__ == "__main__":
    args = parse_arguments()
    main(
        args.employees_file,
        args.previous_file,
        args.output_file,
    )