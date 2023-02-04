from src.models.path_type import PathType


class BundleError(Exception):
    pass


class PathError(Exception):
    def __init__(self, message: str, path_type: PathType):
        super().__init__(message)
        self.path_type = path_type
