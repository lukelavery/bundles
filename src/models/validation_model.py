import os
from src.models.exceptions import PathError


class PathModel:
    @property
    def input_path(self):
        return self.__input_path

    @property
    def output_path(self):
        return self.__output_path

    @input_path.setter
    def input_path(self, value: str):
        self._validate_path(value)
        self.__input_path = value

    @output_path.setter
    def output_path(self, value: str):
        self._validate_path(value)
        self.__output_path = value

    def _validate_path(self, value: str):
        """
        Validate the input_path
        :param value:
        :return:
        """
        if value == '':
            raise PathError('Please select a directory.')
        if not os.path.isdir(value):
            raise PathError('Directory does not exist.')
