"""Tests for SecretSantaService."""

import pytest
from src.models.employee import Employee
from src.services.secret_santa_service import SecretSantaService
from src.exceptions.custom_exceptions import NoValidAssignmentError


class TestSecretSantaService:
    """Test SecretSantaService class."""
    
    def test_valid_assignment_with_two_employees(self):
        """Test assignment with two employees."""
        employees = [
            Employee("Alice", "alice@acme.com"),
            Employee("Bob", "bob@acme.com")
        ]
        service = SecretSantaService(employees, {})
        assignments = service.assign_secret_children()
        
        assert len(assignments) == 2
        assert assignments[0].giver != assignments[0].receiver
        assert assignments[1].giver != assignments[1].receiver
        # Both should be assigned to each other
        assert assignments[0].receiver == assignments[1].giver
        assert assignments[1].receiver == assignments[0].giver
    
    def test_no_self_assignment(self):
        """Test that no one is assigned to themselves."""
        employees = [
            Employee("Alice", "alice@acme.com"),
            Employee("Bob", "bob@acme.com"),
            Employee("Charlie", "charlie@acme.com")
        ]
        service = SecretSantaService(employees, {})
        assignments = service.assign_secret_children()
        
        for assignment in assignments:
            assert assignment.giver != assignment.receiver
    
    def test_no_previous_assignment_repetition(self):
        """Test that no one gets the same person as last year."""
        employees = [
            Employee("Alice", "alice@acme.com"),
            Employee("Bob", "bob@acme.com"),
            Employee("Charlie", "charlie@acme.com")
        ]
        
        previous = {
            Employee("Alice", "alice@acme.com"): Employee("Bob", "bob@acme.com")
        }
        
        service = SecretSantaService(employees, previous)
        assignments = service.assign_secret_children()
        
        for assignment in assignments:
            if assignment.giver.name == "Alice":
                assert assignment.receiver.name != "Bob"
    
    def test_insufficient_employees(self):
        """Test error when fewer than 2 employees."""
        employees = [Employee("Alice", "alice@acme.com")]
        
        with pytest.raises(NoValidAssignmentError):
            SecretSantaService(employees, {})
    
    def test_valid_assignment_covers_all_employees(self):
        """Test that all employees are assigned exactly once."""
        employees = [
            Employee("Alice", "alice@acme.com"),
            Employee("Bob", "bob@acme.com"),
            Employee("Charlie", "charlie@acme.com"),
            Employee("Diana", "diana@acme.com")
        ]
        
        service = SecretSantaService(employees, {})
        assignments = service.assign_secret_children()
        
        # Check all givers are unique
        givers = {a.giver for a in assignments}
        assert len(givers) == len(employees)
        
        # Check all receivers are unique
        receivers = {a.receiver for a in assignments}
        assert len(receivers) == len(employees)
        
        # Check all employees appear as both giver and receiver
        assert givers == set(employees)
        assert receivers == set(employees)