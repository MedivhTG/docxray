class OpcError(Exception):
    pass


class OpcPackageNotFoundError(OpcError):
    pass


class DanglingRelationshipWarning(UserWarning):
    pass
