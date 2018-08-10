"""This file contains custom exceptions"""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class NoProductError(Error):
    """Exception raised if OpenFoodFacts maps don't find results."""
    pass