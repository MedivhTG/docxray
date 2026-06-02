"""Exceptions specific for OPC module."""


class OpcError(Exception):
    """Base error class OPC module."""


class PackageNotFoundError(OpcError):
    """Raised when a package cannot be found at the specified path."""
