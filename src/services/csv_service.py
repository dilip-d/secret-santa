"""CSV file handling service."""

import csv
import os
from typing import List, Optional
from src.models.employee import Employee, Assignment
from src.exceptions.custom_exceptions import FileProcessingError, InvalidInputError


class CSVService:
    """Handles CSV file operations for employee data and assignments."""
    
    REQUIRED_EMPLOYEE_COLUMNS = ['Employee_Name', 'Employee_EmailID']
    REQUIRED_ASSIGNMENT_COLUMNS = ['Employee_Name', 'Employee_EmailID', 
                                   'Secret_Child_Name', 'Secret_Child_EmailID']
    
    @staticmethod
    def read_employees(file_path: str) -> List[Employee]:
        """
        Read employee data from CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            List of Employee objects
            
        Raises:
            FileProcessingError: If file cannot be read or has invalid format
            InvalidInputError: If required columns are missing
        """
        if not os.path.exists(file_path):
            raise FileProcessingError(f"File not found: {file_path}")
        
        employees = []
        
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                if not all(col in reader.fieldnames for col in CSVService.REQUIRED_EMPLOYEE_COLUMNS):
                    raise InvalidInputError(
                        f"CSV must contain columns: {CSVService.REQUIRED_EMPLOYEE_COLUMNS}"
                    )
                
                for row in reader:
                    name = row['Employee_Name'].strip()
                    email = row['Employee_EmailID'].strip()
                    
                    if not name or not email:
                        raise InvalidInputError("Employee name and email cannot be empty")
                    
                    employee = Employee(name=name, email=email)
                    employees.append(employee)
                    
        except csv.Error as e:
            raise FileProcessingError(f"Error reading CSV file: {e}")
        except Exception as e:
            raise FileProcessingError(f"Unexpected error reading file: {e}")
        
        seen = set()
        for emp in employees:
            if emp in seen:
                raise InvalidInputError(f"Duplicate employee found: {emp.name} ({emp.email})")
            seen.add(emp)
        
        return employees
    
    @staticmethod
    def read_previous_assignments(file_path: str) -> dict:
        """
        Read previous year's assignments from CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dictionary mapping giver to receiver (Employee -> Employee)
            
        Raises:
            FileProcessingError: If file cannot be read or has invalid format
        """
        if not os.path.exists(file_path):
            return {}
        
        assignments = {}
        
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                if not all(col in reader.fieldnames for col in CSVService.REQUIRED_ASSIGNMENT_COLUMNS):
                    raise InvalidInputError(
                        f"Previous assignments CSV must contain columns: {CSVService.REQUIRED_ASSIGNMENT_COLUMNS}"
                    )
                
                for row in reader:
                    giver = Employee(
                        name=row['Employee_Name'].strip(),
                        email=row['Employee_EmailID'].strip()
                    )
                    receiver = Employee(
                        name=row['Secret_Child_Name'].strip(),
                        email=row['Secret_Child_EmailID'].strip()
                    )
                    assignments[giver] = receiver
                    
        except csv.Error as e:
            raise FileProcessingError(f"Error reading previous assignments CSV: {e}")
        except Exception as e:
            raise FileProcessingError(f"Unexpected error reading file: {e}")
        
        return assignments
    
    @staticmethod
    def write_assignments(assignments: List[Assignment], output_path: str) -> None:
        """
        Write assignments to CSV file.
        
        Args:
            assignments: List of Assignment objects
            output_path: Path where to save the CSV file
            
        Raises:
            FileProcessingError: If file cannot be written
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['Employee_Name', 'Employee_EmailID', 
                            'Secret_Child_Name', 'Secret_Child_EmailID']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for assignment in assignments:
                    writer.writerow(assignment.to_dict())
                    
        except Exception as e:
            raise FileProcessingError(f"Error writing assignments to file: {e}")