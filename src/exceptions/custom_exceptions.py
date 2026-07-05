"""Custom exceptions for the Secret Santa application."""


class SecretSantaError(Exception):
    """Base exception for Secret Santa application."""
    pass


class InvalidInputError(SecretSantaError):
    """Exception raised for invalid input."""
    pass


class NoValidAssignmentError(SecretSantaError):
    """Exception raised when no valid assignment can be made."""
    pass


class FileProcessingError(SecretSantaError):
    """Exception raised for file processing errors."""
    pass


class DuplicateEmployeeError(SecretSantaError):
    """Exception raised when duplicate employees are found."""
    pass