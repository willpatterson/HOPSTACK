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

class UnknownParameterDeclarationSetting(Exception):
    """Error thrown for unknown type setting in DISS"""
    def __init__(self, message):
        super(UnknownParameterDeclarationSetting, self).__init__(message)

class MulitpleParameterDeclarationSettingError(Exception):
    def __init__(self, message):
        super(MulitpleParameterDeclarationSettingError, self).__init__(message)

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

    Declaration_setting = namedtuple('DeclarationSetting', ['names', 'regex_parse'])
    declaration_settings = {'Level': DeclarationSetting(names=['L', 'Level'], regex_parse='{}([0-9]+)$'),
                            'LevelRequired': DeclarationSetting(names=['Lr', 'LevelRequired'], regex_parse='{}([0-9]+)$'),
                            'Priority': DeclarationSetting(names=['P', 'Priority'], regex_parse='{}([0-9]+)$')}

    def __init__(self, parameter):
        """ """
        parameter = BaseParameter.parse_parameter(parameter)

        self.parameter_type_settings = parameter.parameter_type_settings
        self.target_levels = parameter.parameter_declaration.target_levels
        self.required_level = parameter.parameter_declaration.required_level
        self.priority = parameter.parameter_declaration.priority
        self.allowed_reference_types = parameter.parameter_declaration.allowed_reference_types


    def parse_type_settings(self):
        """To be defined and called by the child classes in __init__"""
        raise NotImplementedError

    @staticmethod
    def factory(parameter):
        """
        Static method that takes a raw parameter statement, creates the proper object type and returns it
        Input : Raw parameter statement
        Output: BaseParameter child object of the type denoted int the parameter_declaration string

        TODO:
        """
        parameter = BaseParameter.parse_parameter(parameter)
        parameter_type = parameter.parameter_declaration.parameter_type

        for cls in BaseParameter.__subclasses__():
            if parameter_type in cls.parameter_type:
                return cls(parameter)

        raise DISSParameterTypeError("Bad parameter type: '{}'".format(parameter_type))

    @staticmethod
    def parse_parameter(parameter):
        """
        Static method that takes a raw parameter statement and parses it completely
        Input : parameter statement (string)
        Output: ParameterStatement Named Tuple
        """
        Parameter = namedtuple('Parameter',
                               ['parameter_declaration', 'parameter_type_settings'])

        #Return parameter ntuple if passed in to avoid double parsing 
        if type(parameter).__name__ is 'Parameter':
            return parameter

        split_statement = parameter.strip('`').split('`')
        if len(split_statement) != 2:
            raise DISSSyntaxError("Parameter statements must have excatly two sections")

        parameter_declaration = BaseParameter.parse_parameter_declaration(split_statement[0])
        parameter_type_settings = re.split(',| ', split_statement[1])
        return ParameterStatement(parameter_declaration=parameter_declaration,
                                  parameter_type_settings=parameter_type_settings)

    @staticmethod
    def parse_parameter_declaration(parameter_declaration):
        """
        Parses a paramter declaration
        Input : raw type statement string
        OutPut: TypeStatement Named Tuple
        TODO:
            Catch and handel exceptions for no int in settings
        """
        ParameterDeclaration = namedtuple('ParameterDeclaration',
                                          ['parameter_type',
                                           'target_levels',
                                           'required_level',
                                           'priority',
                                           'allowed_reference_types'])

        split_declaration = parameter_declaration.split('-')
        tmp_parameter_dec = ParameterDeclaration
        tmp_parameter_dec.parameter_type = split_declaration[0]
        split_declaration.remove(tmp_parameter_dec.parameter_type) #REMOVE the parameter type from the list 

        target_levels = []
        level_requried = None
        priority = None
        allowed_file_references = []
        for declaration_setting in split_declaration:
            tmp_setting = BaseParameter.match_declaration_setting('Level', declaration_setting)
            if tmp_setting:
                target_levels.append(int(tmp_setting))
                continue

            tmp_setting = BaseParameter.match_declaration_setting('LevelRequired', declaration_setting)
            if tmp_setting:
                if level_requried is not None: level_requried = int(tmp_setting)
                else: raise MulitpleParameterDeclarationSettingError("There can only be ONE 'Required Level' set in a 'Parameter Declaration'")
                continue

            tmp_setting = BaseParameter.match_declaration_setting('Priority', declaration_setting)
            if tmp_setting:
                if priority is not None: priority = int(tmp_setting)
                else: raise MulitpleParameterDeclarationSettingError("There can only be ONE 'Priority' setting in a 'Parameter Declaration'")
                continue

            if declaration_setting in [ref for duo in BaseParameter.valid_file_references for ref in duo]:
                allowed_file_references.append(declaration_setting)
            else:
                raise UnknownParameterDeclarationSetting("Error: Unknown parameter declaration setting: {}".format(declaration_setting))

        tmp_parameter_dec.target_levels = target_levels
        tmp_parameter_dec.required_level = required_level
        tmp_parameter_dec.priority = priority
        tmp_parameter_dec.allowed_file_references = allowed_file_references
        return tmp_parameter_dec

    @staticmethod
    def match_declaration_setting(declaration_setting_name, declaration_setting):
        """
        Input: Takes a declaration setting name to access data from, the string to look for the declaration setting name in
        Output: Returns the desired setting value if setting type is a match, returns None if nothing found
        """
        for name in BaseParameter.declaration_settings[declaration_settings].names:
            search = re.search(BaseParameter.declaration_settings[declaration_setting].regex_parse.format(name), declaration_setting)
            if search:
                return search.group(1)
        return ""


    @staticmethod
    def split_settings(settings):
        parameter_settings = re.split(',| ', parameter_declaration.type_settings)


class RegexFilter(BaseParameter):
    """Parameter object that filters strings with a python regex"""
    parameter_type = ('re', 'regex')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class ExentionFilter(BaseParameter):
    """Parameter object that filters verified file paths by extention"""
    parameter_type = ('e', 'extention')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class SubstringFilter(BaseParameter):
    """Parameter object that filters all strings by substring inclusion"""
    parameter_type = ('s', 'substring')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RangeFilter(BaseParameter):
    """Parameter object that filters out all files not in the specified range"""
    parameter_type = ('r', 'range')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RangeUniqueFilter(BaseParameter):
    """Parameter object that filters out all files not in the specified range but will throw error if not all number in range found"""
    parameter_type = ('ru', 'range_unique')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class SinFileParameter(BaseParameter):
    """Takes in a sin file, returns its contents iteratively"""
    parameter_type = ('sin', 'station_in')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RawDelimiter(BaseParameter):
    """Parameter object that opens files and returns chuncks of delimited text"""
    parameter_type = ('rd', 'raw_dilimeter')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class TargetLevels(BaseParameter):
    """Parameter object that dictates operations on a target level"""
    parameter_type = ('tl', 'target_levels')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class HyperlinkFilter(BaseParameter):
    """Parameter object that searches for and returns hyperlinks on webpages"""
    parameter_type = ('h', 'hyperlink')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)
    def parse_type_settings(self):
        """"""
        raise NotImplementedError



if __name__ == '__main__':
    ################# TESTING ##################

    # Data Statement Parameter parsing tests
    #### Factory Test: PASSED!!
    parameter_type = "r"
    parameter_declaration = "`r`stuff`"
    print(type(BaseParameter.factory(parameter_declaration)))

    #### Basic parameter
    #### Compound parameter
    #### Multiple parameters

    # Full Data statement parsing tests

    # LASDI file path tests

    # LASDI Raw Data tests

    pass


