class UpdateReqSpecException(Exception):
    pass


class InvalidSetupFile(UpdateReqSpecException):
    pass


class PackageNotFound(UpdateReqSpecException):
    pass
