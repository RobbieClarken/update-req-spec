class RepinException(Exception):
    pass


class InvalidSetupFile(RepinException):
    pass


class PackageNotFound(RepinException):
    pass
