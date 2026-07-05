"""Secret Santa assignment service."""

import random
from typing import List, Set, Optional, Dict
from src.models.employee import Employee, Assignment
from src.exceptions.custom_exceptions import NoValidAssignmentError


class SecretSantaService:
    """Handles the Secret Santa assignment logic."""
    
    def __init__(self, employees: List[Employee], previous_assignments: Optional[Dict[Employee, Employee]] = None):
        """
        Initialize the Secret Santa service.
        
        Args:
            employees: List of employees participating
            previous_assignments: Dictionary of previous year's assignments
        """
        self.employees = employees
        self.previous_assignments = previous_assignments or {}
        self._validate_employees()
        
    def _validate_employees(self) -> None:
        """Validate that there are enough employees for the game."""
        if len(self.employees) < 2:
            raise NoValidAssignmentError("At least 2 employees are required for Secret Santa")
    
    def _is_valid_assignment(self, giver: Employee, receiver: Employee) -> bool:
        """
        Check if an assignment is valid.
        
        An assignment is valid if:
        1. The giver is not assigning to themselves
        2. The giver is not assigning to the same person as last year
        """
        if giver == receiver:
            return False

        if giver in self.previous_assignments and self.previous_assignments[giver] == receiver:
            return False
        
        return True
    
    def assign_secret_children(self) -> List[Assignment]:
        """
        Assign secret children to all employees.
        
        Returns:
            List of Assignment objects
            
        Raises:
            NoValidAssignmentError: If no valid assignment can be made
        """
        available_receivers = self.employees.copy()
        assignments = []

        random.shuffle(self.employees)
        random.shuffle(available_receivers)

        assignment_map = {}
        receivers_set = set(self.employees)

        for attempt in range(100):
            assignment_map.clear()
            receivers_set = set(self.employees)
            random.shuffle(self.employees)
            
            success = True
            for giver in self.employees:
                valid_receivers = [
                    r for r in receivers_set
                    if self._is_valid_assignment(giver, r)
                ]

                if not valid_receivers:
                    success = False
                    break

                receiver = random.choice(valid_receivers)
                assignment_map[giver] = receiver
                receivers_set.remove(receiver)
            
            if success and len(assignment_map) == len(self.employees):
                break
        
        if len(assignment_map) != len(self.employees):
            raise NoValidAssignmentError(
                "Could not find valid Secret Santa assignments. "
                "This might be due to too few employees or restrictive previous assignments."
            )
        
        return [Assignment(giver=giver, receiver=receiver)
                for giver, receiver in assignment_map.items()]