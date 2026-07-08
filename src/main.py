"""Main entry point for the Secret Santa application."""

import os
import sys
import argparse
from typing import Optional
from src.services.csv_service import CSVService
from src.services.secret_santa_service import SecretSantaService
from src.exceptions.custom_exceptions import SecretSantaError, FileProcessingError


def main(employees_file: str, previous_assignments_file: Optional[str] = None,
         output_file: Optional[str] = None) -> None:
    """
    Main function to run the Secret Santa assignment.
    
    Args:
        employees_file: Path to employees CSV file
        previous_assignments_file: Path to previous assignments CSV file (optional)
        output_file: Path to output CSV file (optional)
    """
    try:
        employees = CSVService.read_employees(employees_file)

        previous_assignments = {}
        if previous_assignments_file and os.path.exists(previous_assignments_file):
            previous_assignments = CSVService.read_previous_assignments(previous_assignments_file)

        service = SecretSantaService(employees, previous_assignments)
        assignments = service.assign_secret_children()

        if output_file is None:
            output_file = "output/secret_santa_assignments.csv"
        CSVService.write_assignments(assignments, output_file)

    except FileProcessingError:
        sys.exit(1)
    except SecretSantaError:
        sys.exit(1)
    except Exception:
        sys.exit(1)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Secret Santa Assignment System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py data/employees.csv
  python main.py data/employees.csv --previous data/previous_assignments.csv
  python main.py data/employees.csv --previous data/previous_assignments.csv --output output/new_assignments.csv
        """
    )
    
    parser.add_argument(
        'employees_file',
        help='Path to CSV file containing employee information'
    )
    
    parser.add_argument(
        '--previous', '-p',
        dest='previous_file',
        help='Path to CSV file containing previous year\'s assignments (optional)'
    )
    
    parser.add_argument(
        '--output', '-o',
        dest='output_file',
        help='Path to output CSV file (default: output/secret_santa_assignments.csv)'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args.employees_file, args.previous_file, args.output_file)