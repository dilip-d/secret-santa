"""Employee model module."""

from dataclasses import dataclass


@dataclass
class Employee:
    """Represents an employee with their basic information."""
    
    name: str
    email: str
    
    def __hash__(self):
        """Allow Employee to be used as a dictionary key."""
        return hash((self.name, self.email))
    
    def __eq__(self, other):
        """Compare two employees by name and email."""
        if not isinstance(other, Employee):
            return False
        return self.name == other.name and self.email == other.email


@dataclass
class Assignment:
    """Represents a Secret Santa assignment."""
    
    giver: Employee
    receiver: Employee
    
    def to_dict(self):
        """Convert assignment to dictionary format for CSV export."""
        return {
            'Employee_Name': self.giver.name,
            'Employee_EmailID': self.giver.email,
            'Secret_Child_Name': self.receiver.name,
            'Secret_Child_EmailID': self.receiver.email
        }