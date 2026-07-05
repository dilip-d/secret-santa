"""Tests for Employee model."""

import pytest
from src.models.employee import Employee, Assignment


class TestEmployee:
    """Test Employee class."""
    
    def test_employee_creation(self):
        """Test creating an employee."""
        emp = Employee("John Doe", "john@acme.com")
        assert emp.name == "John Doe"
        assert emp.email == "john@acme.com"
    
    def test_employee_equality(self):
        """Test employee equality comparison."""
        emp1 = Employee("John Doe", "john@acme.com")
        emp2 = Employee("John Doe", "john@acme.com")
        emp3 = Employee("Jane Doe", "jane@acme.com")
        
        assert emp1 == emp2
        assert emp1 != emp3
        assert hash(emp1) == hash(emp2)
        assert hash(emp1) != hash(emp3)
    
    def test_assignment_creation(self):
        """Test creating an assignment."""
        giver = Employee("John Doe", "john@acme.com")
        receiver = Employee("Jane Doe", "jane@acme.com")
        assignment = Assignment(giver, receiver)
        
        assert assignment.giver == giver
        assert assignment.receiver == receiver
    
    def test_assignment_to_dict(self):
        """Test converting assignment to dictionary."""
        giver = Employee("John Doe", "john@acme.com")
        receiver = Employee("Jane Doe", "jane@acme.com")
        assignment = Assignment(giver, receiver)
        
        expected = {
            'Employee_Name': 'John Doe',
            'Employee_EmailID': 'john@acme.com',
            'Secret_Child_Name': 'Jane Doe',
            'Secret_Child_EmailID': 'jane@acme.com'
        }
        assert assignment.to_dict() == expected