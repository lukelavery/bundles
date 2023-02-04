import os
from src.models.path_type import PathType

from src.models.exceptions import PathError


class PathModel:
    def __init__(self, value: str):
        self.input_path = value
        # self.output_path = 'None'

    @property
    def input_path(self):
        return self.__input_path

    # @property
    # def output_path(self):
    #     return self.__output_path

    @input_path.setter
    def input_path(self, value: str):
        self.__input_path = self._validate_path(
            value=value,
            path_type=PathType.INPUT,
        )

    # @output_path.setter
    # def output_path(self, value: str):
    #     self.__output_path = self._validate_path(
    #         value=value,
    #         path_type=PathType.OUTPUT,
    #     )

    def _validate_path(self, value: str, path_type: PathType):
        """
        Validate the path
        :param value:
        :return:
        """
        if value == '':
            raise PathError(
                message='Please select a directory.',
                path_type=path_type,
            )
        if not os.path.isdir(value):
            raise PathError(
                message='Directory does not exist.',
                path_type=path_type,
            )
        return value
