"""
Main file for the LASubway Data Interpreter (LASDI)

TODO:
    - Implement DISS
    - Implement network file downloads
    - Implement file-path search on the "Metro Network" if a path is not found on file system
    - Implement local file path search within the metro directory **I now have doubts about this
"""

import os
import re
import ntpath
from collections import namedtuple
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

# Data Statement Classes: #############################################

class DISSSyntaxError(Exception):
    """Error thrown for bad DISS syntax"""
    def __init__(self, message):
        super(DISSSyntaxError, self).__init__(message)

class DISSParameterTypeError(Exception):
    """Error thrown when the Parameter type string is incorrect"""
    def __init__(self, message):
        super(DISSParameterTypeError, self).__init__(message)

class UnknownTypeSetting(Exception):
    """Error thrown for unknown type setting in DISS"""
    def __init__(self, message):
        super(DISSSyntaxError, self).__init__(message)


class DataReference(ParseResult):
    """
    This class will be used for parsing and operating a single Data Reference
    """
    def __init__(self, reference):
        """
        TODO:
            Parse out Data Filters before passing the string to urlparse
        """
        if (== "" or reference is None):
            raise Exception #TODO Create exception for this

        self.parameters = []
        split_reference = reference.split('`')
        data_string = urlparse(split_reference[0])
        super.__init__([getattr(data_string, field) for field in data_string._fields]) #TODO add user name and password info 

    @staticmethod
    def _load_parameters(parameters):
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


class BaseParameter(object):
    """
    Base parameter object

    TODO:
        Change variable names to fit new system
    """
    valid_file_references = [('f','file'),
                             ('f', 'directory'),
                             ('l', 'symlink'),
                             ('r', 'raw_text'),
                             ('t', 'tar_archive'),
                             ('g', 'gzip'),
                             ('b', 'bz2'),
                             ('z', 'zip'),
                             ('u', 'url'),
                             ('p', 'pipe'),
                             ('s', 'socket')]

    def __init__(self, parameter_statement):
        """ """
        parameter_statement = BaseParameter.parse_parameter_statement(parameter_statement)

        self.parameter_type_settings = re.split(',| ', parameter_statement.type_settings)
        self.level_limit = parameter_statement.type_statement.level_limit
        self.level_requried = parameter_statement.type_statement.level_requried
        self.priority = parameter_statement.type_statement.priority
        self.allowed_reference_types = parameter_statement.type_statement.allowed_reference_types


    def parse_type_settings(self):
        """To be defined and called by the child classes in __init__"""
        raise NotImplementedError

    @staticmethod
    def factory(parameter_statement):
        """
        Static method that takes a raw parameter statement, creates the proper object type and returns it
        Input : Raw parameter statement
        Output: BaseParameter child object of the type denoted int the parameter_statement string

        TODO:
        """
        parsed_parameter_statement = BaseParameter.parse_parameter_statement(parameter_statement)
        parameter_type = parsed_parameter_statement.type_statement.parameter_type

        for cls in BaseParameter.__subclasses__():
            if parameter_type in cls.parameter_type:
                return cls(parameter_statement)

        raise DISSParameterTypeError("Bad parameter type: '{}'".format(parameter_type))

    @staticmethod
    def parse_parameter_statement(parameter_statement):
        """
        Static method that takes a raw parameter statement and parses it completely
        Input : parameter statement (string)
        Output: ParameterStatement Named Tuple
        """
        ParameterStatement = namedtuple('ParameterStatement',
                                        ['type_statement', 'type_settings'])

        split_statement = parameter_statement.strip('`').split('`')
        if len(split_statement) != 2:
            raise DISSSyntaxError("Parameter statements must have excatly two sections")

        parsed_type_statement = BaseParameter.parse_type_statement(split_statement[0])
        parameter_statement = ParameterStatement(type_statement=parsed_type_statement,
                                                 type_settings=split_statement[1])

        return parameter_statement

    @staticmethod
    def parse_type_statement(parameter_type_statement):
        """
        Parses a type statement
        Input : raw type statement string
        OutPut: TypeStatement Named Tuple
        TODO:
            Catch and handel exceptions for no int in settings
            Catch and handle exceptions for imporper statements when stripping integers
            Reconsider benifits of removing items from list
            Consider creating a fucntion to combine searching for Level limits and priority
            Change level_limit to target_level
            Provide support for multiple level targets in one statement
            Only provide support for a single required level
        """
        TypeStatement = namedtuple('TypeStatement',
                                   ['parameter_type',
                                    'level_limit',
                                    'level_requried',
                                    'priority',
                                    'allowed_reference_types'])

        split_statement = parameter_type_statement.split('-')
        psettings = TypeStatement
        psettings.parameter_type = split_statement[0]
        split_statement.remove(psettings.parameter_type) #REMOVE ITEM FROM LIST

        #Parses Out level interception settings
        #TODO catch and handel exceptions for no int 
        level_limit = [x for x in split_statement if x.startswith('L')]
        if len(level_limit) > 1:
            raise Exception #Exception for having multiple level limit statements
        elif len(level_limit) == 0:
            psettings.level_limit = None
            psettings.level_requried = False
        elif len(level_limit) == 1:
            level_limit = level_limit[0]
            split_statement.remove(level_limit) #REMOVE ITEM FROM LIST
            if level_limit.startswith('Lr'):
                psettings.level_requried = True
            level_limit = int("".join(i for i in level_limit if x.isdigit())) #Integer stripping
            psettings.level_limit = level_limit

        priority = [x for x in split_statement if x.startswith('P')]
        if len(priority) > 1:
            raise Exception #Exception for having multiple priority statements
        elif len(priority) == 0:
            psettings.priority = None
        elif len(priority) == 1:
            priority = priority[0]
            split_statement.remove(priority[0]) #REMOVE ITEM FROM LIST
            priority = int("".join(i for i in level_limit if x.isdigit())) #Integer stripping
            psettings.priority = priority

        #Check for valid reference types
        for reference_type in split_statement:
            if reference_type in [ref for duo in BaseParameter.valid_file_references for ref in duo]:
                if type(psettings.allowed_reference_types) == str:
                    psettings.allowed_reference_types = [psettings.allowed_reference_types, reference_type]
                else:
                    psettings.allowed_reference_types = reference_type
            else:
                raise UnknownTypeSetting("Error: Unknown type setting: {}".format(reference_type))

        return psettings

    @staticmethod
    def split_settings(settings):
        parameter_settings = re.split(',| ', parameter_statement.type_settings)


class RegexFilter(BaseParameter):
    """Parameter object that filters strings with a python regex"""
    parameter_type = ('re', 'regex')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class ExentionFilter(BaseParameter):
    """Parameter object that filters verified file paths by extention"""
    parameter_type = ('e', 'extention')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class SubstringFilter(BaseParameter):
    """Parameter object that filters all strings by substring inclusion"""
    parameter_type = ('s', 'substring')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RangeFilter(BaseParameter):
    """Parameter object that filters out all files not in the specified range"""
    parameter_type = ('r', 'range')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RangeUniqueFilter(BaseParameter):
    """Parameter object that filters out all files not in the specified range but will throw error if not all number in range found"""
    parameter_type = ('ru', 'range_unique')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class SinFileParameter(BaseParameter):
    """Takes in a sin file, returns its contents iteratively"""
    parameter_type = ('sin', 'station_in')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RawDelimiter(BaseParameter):
    """Parameter object that opens files and returns chuncks of delimited text"""
    parameter_type = ('rd', 'raw_dilimeter')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class TargetLevel(BaseParameter):
    """Parameter object that dictates operations on a target level"""
    parameter_type = ('tl', 'target_level')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class HyperlinkFilter(BaseParameter):
    """Parameter object that searches for and returns hyperlinks on webpages"""
    parameter_type = ('h', 'hyperlink')
    def __init__(self, parameter_statement):
        super().__init__(parameter_statement)
    def parse_type_settings(self):
        """"""
        raise NotImplementedError



if __name__ == '__main__':
    ################# TESTING ##################

    # Data Statement Parameter parsing tests
    #### Factory Test: PASSED!!
    parameter_type = "r"
    parameter_statement = "`r`stuff`"
    print(type(BaseParameter.factory(parameter_statement)))

    #### Basic parameter
    #### Compound parameter
    #### Multiple parameters

    # Full Data statement parsing tests

    # LASDI file path tests

    # LASDI Raw Data tests

    pass


