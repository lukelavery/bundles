import os
from models.exceptions import ValidationError


class ValidationModel:
    @property
    def input_path(self):
        return self.__input_path

    @input_path.setter
    def input_path(self, value):
        """
        Validate the input_path
        :param value:
        :return:
        """
        if value == '':
            raise ValidationError('Please select a directory.')
        if os.path.isdir(value):
            self.__input_path = value
        else:
            raise ValidationError('Directory does not exist.')

    @property
    def output_path(self):
        return self.__output_path

    @output_path.setter
    def output_path(self, value):
        """
        Validate the input_path
        :param value:
        :return:
        """
        if value == '':
            raise ValidationError('Please select a directory.')
        if os.path.isdir(value):
            self.__input_path = value
        else:
            raise ValidationError('Directory does not exist.')
