"""
Main file for the LASubway Data Interpreter (LASDI)

TODO:
    - Implement DISS
    - Implement network file downloads
    - Implement file-path search on the "Metro Network" if a path is not found on file system
    - Implement local file path search within the metro directory **I now have doubts about this
"""

import os
import ntpath
#import urllib
from urllib.parse import urlparse, ParseResult

#Imports for compression/archive file interpreting:
import gzip
import bz2
import zipfile
import tarfile

class IndecipherableStringError(Exception):
    """Error when a string cannot be desciphered"""
    def __init__(self, message):
        super(IndecipherableStringError, self).__init__(message)

def data_interpreter(data_string, tmp_data_dump):
    """Generates a string(s) to pass to a station to be used as the input path(s)"""

    if os.path.isfile(data_string):
        comp_file = check_compression(data_string)
        if comp_file != None:
            return extract_compresson_files(comp_file, tmp_data_dump)

        elif tarfile.is_tarfile(data_string):
            return extract_tar_files(data_string, tmp_data_dump)
        elif data_string.endswith("_staion_input.sin"):
            return extract_sin_files(data_string)
        else:
            return data_string #This is where recursive calls end

    #TODO Implement Network downloads
    #TODO Implement automatic metro execution

    elif os.path.isdir(data_string):
        #if is_metro(data_string): TODO Implement please
        #    return run_metro(data_string)  
        return extract_dir_files()

    else:
        raise IndecipherableStringError("Indecipherable string!!!")

def extract_sin_files(sin_path, out_directory):
    """
    Opens a Station Input File and returns a list of verified input strings
    (A Station file contains filepaths to other files. extention: .sin)
    """

    in_strings = []
    with open(sin_path, 'r') as sinfile:
        for line in sinfile:
            return data_interpreter(line, out_directory)

def extract_dir_files(dir_path, out_directory):
    """Opens a directory and returns a list of verified input strings"""

    for path in [os.path.join(dir_path, i) for i in os.listdir(dir_path)]:
        return data_interpreter(path, out_directory)

def extract_tar_files(tar_file, out_directory):
    """
    extracts all files in a tar archive
    """
    tar_name = ntpath.basename(tar_file)
    un_tar_path = os.path.join(tar_file, tar_name)
    tarfile.TarFile(tar_file)
    tarfile.extractall(out_directory)

    return data_interpreter(un_tar_path, out_directory)

def extract_zip_files(zip_file, out_directory):
    """
    extracts all files in a zip archive
    """
    zip_name = ntpath.basename(zip_file)
    un_tar_path = os.path.join(zip_file, zip_name)
    zipfile.TarFile(zip_file)
    zarfile.extractall(out_directory)

    return data_interpreter(un_tar_path, out_directory)

def extract_compresson_file(compression_file, out_directory):
    """
    Attempts to decompress a filepath
    Will pass higher file types to data_interpreter before returning
    """
    out_file_name = ntpath.basename(compression_file.path)
    out_file_name_path = os.path.join(out_directory, out_file_name)
    with open(out_file_name_path, 'w') as f:
        f.write(compression_file.decompress())
    return data_interpreter(out_file_name_path, out_directory)

def check_compression(filename):
    """
    Function that attempts to detect and compression type
    The code used was found at: http://stackoverflow.com/questions/13044562/python-mechanism-to-identify-compressed-file-type-and-uncompress
    """
    with file(filename, 'rb') as f:
        start_of_file = f.read(1024)
        f.seek(0)
        for cls in (BZ2File, GZFile):
            if cls.is_magic(start_of_file):
                return cls(f)

        return None

#Classes for file compression detection and decompression
class CompressedFile(object):
    magic_signature = None
    filetype = None
    default_extention = None

    def __init__(self, path):
        self.path = path
        self.accessor = self.open()

    def is_magic(self, file_start):
        return file_start.startswith(self.magic_signature)

    def decompress(self):
        raise NotImplementedError

class GZFile(CompressedFile):
    magic_signature = "\x1f\x8b\x08"
    filetype = "gzip"
    default_extention = ".gz"

    def decompress(self):
         with gzip.open(self.path, 'rb') as gfile:
             return gfile.read()

class BZ2File(CompressedFile):
    magic_signature = "\x42\x5a\x68"
    filetype = "bzip2"
    default_extention = ".bz2"

    def decompress(self, outpath):
        with bz2.open(self.path, 'rb') as bfile:
            return bfile.read()


def diss_interpreter(data_string):
    """Parses out filter statments denoted by `"""
    split_data = data_string.split('`')

class DataStatement(ParseResult):
    """
    This class will be used for parsing and operating a single data statement
    """
    def __init__(self, statement_string):
        """
        TODO:
            Parse out Data Filters before passing the string to urlparse
        """
        if (statement_string == "" or statement_string is None):
            raise Exception #TODO Create exception for this

        self.parameters = []
        parsed_statement = statement_string.split('`')
        parsed_data_string = urlparse(parsed_statement[0])
        super.__init__([getattr(parsed_data_string, field) for field in parsed_data_string._fields]) #TODO add user name and password info 

    @staticmethod
    def _create_data_parameters(parameters):
        pass

    def is_local(self):
        """
        RETURNS TRUE: if self.path is the only field that is set (assuming that empty strings are caught)
        RETURNS FALSE: if other fields besides self.path are set
        TODO:
            this needs to be fully tested
        """

        if (self.scheme == ""
            and self.netloc == ""
            and self.params == ""
            and self.query == ""
            and self.fragment == ""):
            return True
        return False


class DISSSyntaxError(Exception):
    """Error thrown for bad DISS syntax"""
    def __init__(self, message):
        super(DISSSyntaxError, self).__init__(message)

class DISSParameterTypeError(Exception):
    """Error thrown when the Parameter type string is incorrect"""
    def __init__(self, message):
        super(DISSParameterTypeError, self).__init__(message)

#Data String Classes: #############################################

class BaseParameter(object):
    """Base parameter object"""
    def __init__(self, parameter_type, parameter_statement):
        self.parameter_statement = parameter_statement
        self.parameter_type = parameter_type

        self.level_limit = None
        self.level_requried = False
        self.priority = None
        self.allowed_reference_types = []

        if (self.parameter_statement.count != 3) or ((not self.parameter_statement.startswith('`')) and (not self.parameter_statement.endswith('`'))):
            raise DISSSyntaxError
        elif self.parse_parameter_statement()[0] != self.parameter_type:
            raise DISSParameterTypeError


    def factory(parameter_type):
        """"""
        if (parameter_type == 're') or (parameter_type == 'regex'): return RegexFilter()
        if (parameter_type == 'r') or (parameter_type == 'range'): return RangeFilter()
        if (parameter_type == 'ru') or (parameter_type == 'range-unique'): return RangeUniqueFilter()
        if (parameter_type == 'e') or (parameter_type == 'extention'): return ExentionFilter()
        if (parameter_type == 's') or (parameter_type == 'substring'): return SubstringFilter()
        if (parameter_type == 'sin') or (parameter_type == 'station-in-file'): return SinFileParameter()
        if (parameter_type == 'rd') or (parameter_type == 'raw-delimiter'): return RawDelimiter()

        assert 0, "Bad parameter: " + parameter_type
    factory = staticmethod(factory)

    def parse_parameter_statement(self):
        """"""
        return self.parameter_statement.split('`')

    @staticmethod
    def parse_parameter_type_settings(parameter_type_statement):
        """
        This method will parse out the settings defined after parameter type but in the parameter type field
        """
        split_statement = parameter_type_statement.split('-')
        parameter_type = split_statement[0]



class RegexFilter(BaseParameter):
    """Parameter object that filters strings with a python regex"""
    def __init__(self, parameter_statement):
        super().__init__('re', parameter_statement)

class ExentionFilter(BaseParameter):
    """Parameter object that filters verified file paths by extention"""
    def __init__(self, parameter_statement):
        super().__init__('e', parameter_statement)

class SubstringFilter(BaseParameter):
    """Parameter object that filters all strings by substring inclusion"""
    def __init__(self, parameter_statement):
        super().__init__('s', parameter_statement)

class RangeFilter(BaseParameter):
    """Parameter object that filters out all files not in the specified range"""
    def __init__(self, parameter_statement):
        super().__init__('r', parameter_statement)

class RangeUniqueFilter(BaseParameter):
    """Parameter object that filters out all files not in the specified range but will throw error if not all number in range found"""
    def __init__(self, parameter_statement):
        super().__init__('ru', parameter_statement)

class SinFileParameter(BaseParameter):
    """"""
    def __init__(self, parameter_statement):
        super().__init__('sin', parameter_statement)

class RawDelimiter(BaseParameter):
    """"""
    def __init__(self, parameter_statement):
        super().__init__('rd', parameter_statement)

class LevelIntercept(BaseParameter):
    """"""
    def __init__(self, parameter_statement):
        super().__init__('L', parameter_statement)



if __name__ == '__main__':
    ################# TESTING ##################

    # Data Statement Parameter parsing tests
    #### Factory Test
    parameter_type = "r"
    print(type(BaseParameter.factory(parameter_type)))

    #### Basic parameter
    #### Compound parameter
    #### Multiple parameters

    # Full Data statement parsing tests

    # LASDI file path tests

    # LASDI Raw Data tests

    pass


