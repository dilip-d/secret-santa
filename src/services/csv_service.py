"""CSV and Excel file handling service."""

import csv
import os
import zipfile
import xml.etree.ElementTree as ET
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
        Read previous year's assignments from a CSV or XLSX file.
        
        Args:
            file_path: Path to the CSV or XLSX file
            
        Returns:
            Dictionary mapping giver to receiver (Employee -> Employee)
            
        Raises:
            FileProcessingError: If file cannot be read or has invalid format
        """
        if not os.path.exists(file_path):
            return {}

        if file_path.lower().endswith('.xlsx'):
            return CSVService.read_assignments(file_path)

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
    def read_assignments(file_path: str) -> List[Assignment]:
        """Read assignments from a CSV or XLSX file."""
        if not os.path.exists(file_path):
            raise FileProcessingError(f"File not found: {file_path}")

        if file_path.lower().endswith('.xlsx'):
            return CSVService._read_assignments_from_xlsx(file_path)

        assignments = []
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                if not all(col in reader.fieldnames for col in CSVService.REQUIRED_ASSIGNMENT_COLUMNS):
                    raise InvalidInputError(
                        f"Assignments CSV must contain columns: {CSVService.REQUIRED_ASSIGNMENT_COLUMNS}"
                    )

                for row in reader:
                    giver = Employee(name=row['Employee_Name'].strip(), email=row['Employee_EmailID'].strip())
                    receiver = Employee(name=row['Secret_Child_Name'].strip(), email=row['Secret_Child_EmailID'].strip())
                    assignments.append(Assignment(giver=giver, receiver=receiver))
        except csv.Error as e:
            raise FileProcessingError(f"Error reading assignments CSV: {e}")
        except Exception as e:
            raise FileProcessingError(f"Unexpected error reading file: {e}")

        return assignments

    @staticmethod
    def _read_assignments_from_xlsx(file_path: str) -> List[Assignment]:
        try:
            with zipfile.ZipFile(file_path) as archive:
                shared_strings = []
                if 'xl/sharedStrings.xml' in archive.namelist():
                    root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
                    ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    for si in root.findall('a:si', ns):
                        texts = [t.text or '' for t in si.iter() if t.tag.endswith('}t')]
                        shared_strings.append(''.join(texts))

                workbook = ET.fromstring(archive.read('xl/workbook.xml'))
                rels = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
                rel_ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                rel_map = {rel.attrib['Id']: rel.attrib['Target'] for rel in rels.findall('r:Relationship', rel_ns)}
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

                sheet = workbook.find('a:sheets', ns).find('a:sheet', ns)
                rel = rel_map[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
                sheet_path = 'xl/' + rel if not rel.startswith('xl/') else rel
                data = ET.fromstring(archive.read(sheet_path))

                assignments = []
                for row in data.findall('.//a:sheetData/a:row', ns):
                    values = []
                    for cell in row.findall('a:c', ns):
                        cell_type = cell.attrib.get('t')
                        value_node = cell.find('a:v', ns)
                        value = value_node.text if value_node is not None else ''
                        if cell_type == 's' and value is not None:
                            value = shared_strings[int(value)]
                        values.append(value)

                    if len(values) < 4:
                        continue
                    if values[0] == 'Employee_Name':
                        continue
                    giver = Employee(name=values[0].strip(), email=values[1].strip())
                    receiver = Employee(name=values[2].strip(), email=values[3].strip())
                    assignments.append(Assignment(giver=giver, receiver=receiver))
        except Exception as e:
            raise FileProcessingError(f"Error reading assignments from Excel file: {e}")

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