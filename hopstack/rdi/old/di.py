"""
Main file for the LASubway Data Interpreter (LASDI)

TODO:
    - Refactor DataReference and BaseParameter into functional implementations
    - Implement network file downloads
    - Implement file-path search on the "Metro Network" if a path is
      not found on file system
      **what?
    - Implement local file path search within the metro directory
      **I now have doubts about this
"""

import os
import shutil
import re
import ntpath
from collections import namedtuple

import urllib
from urllib.parse import urlparse, urlunparse, ParseResult
from urllib.request import urlopen
from contextlib import closing

#Imports for compression/archive file interpreting:
import gzip
import bz2
import zipfile
import tarfile

def data_interpreter(data_string, tmp_data_dump):
    """
    finds data with a Data Reference object and returns desired output
    if found

    TODO:
        Implement recursive execution of LASOs
        Implement URL parseing
        Implement DataReference Class
    """

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

    elif os.path.isdir(data_string):
        return extract_dir_files()

    else:
        raise TypeError("Indecipherable string!!!")


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

# LASDI Classes: ##############################################################

class DataInterpreter(object):
    """Defines LASDI"""
    def __init__(self):
        pass

# Data Reference Classes: #####################################################
class DataReference(ParseResult):
    """
    This class will be used for parsing and operating a single Data Reference
    Inherits from urllib's ParseResult

    Duties of DataReference:
        1) Parse Data References into: URL and Parameters
        2) Create and store Parameter Objects
        3) Fetch parse and filter data found with the URL
    TODO:
        support escape sequence for '`'
        Consider passing station instead of metro and moving url generation
            methods to a station objects
    """

    def __init__(self, reference, metro=None):
        """
        TODO:
        """
        if (reference == "" or reference is None):
            raise ValueError

        split_reference = reference.strip('`').split('`')
        url = urlparse(split_reference[0])
        split_reference.remove(split_reference[0])

        if url.scheme == '':
            url.scheme == 'file'

        # Translate URL if using custom scheme 
        # Should probably completely refactor this.
        # workspaces should be managed by LASWSA, not a metro object
        try:
            if self.scheme == "wrkspace":
                url = self.metro.generate_workspace_url(self.path)
            elif self.scheme == "prelaso":
                url = self.metro.generate_previous_laso_url(self.path)
        except AttributeError:
            assert 0, "Error: Data Reference must be run inside a metro to use schemes: wrkspace, prelaso" #TODO Create proper exception

        parameters = []
        i = 0
        while i<len(split_reference):
            parameters.append('`'.join([split_reference[i], split_reference[i+1]]))
            i+=2

        self.parameters = BaseParameter.factory(parameters)

        super.__init__([getattr(data_string, field) for field in data_string._fields]) #TODO add user name and password info 

    def is_local(self):
        """
        RETURNS TRUE: if self.path is the only field that is set
            (assuming that empty strings are caught)
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

    def get_data(self, save_directory):
        """
        Retrieves data from remote location
        saves data in: save_directory
        TODO:
            figure out how to handle local file paths
            consider directory downloads from html pages with hyperlinks
            ** Impliment custom URL schemes -- Now needs to be done in lasubway.py
            How does raw data fit into this function?
        """

        url = urlunparse(self)
        file_name = os.path.basename(os.path.normpath(self.path))
        save_path = os.path.join(save_directory, file_name)
        with closing(urlopen(url)) as request:
            with open(save_path, 'wb') as sfile:
                shutil.copyfileobj(request, sfile)


class BaseParameter(object):
    """
    Base parameter object

    TODO:
        Change variable names to fit new system
        support escape sequence for '`'
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

    DeclarationSetting = namedtuple('DeclarationSetting',
                                     ['names', 'regex_parse'])

    declaration_settings = {'Level':
                            DeclarationSetting(names=['L', 'Level'],
                                               regex_parse='{}([0-9]+)$'),
                            'LevelRequired':
                            DeclarationSetting(names=['Lr', 'LevelRequired'],
                                               regex_parse='{}([0-9]+)$'),
                            'Priority':
                            DeclarationSetting(names=['P', 'Priority'],
                                               regex_parse='{}([0-9]+)$')}

    def __init__(self, parameter):
        """ """
        parameter = BaseParameter.parse_parameter(parameter)

        self.parameter_type_settings = parameter.type_settings
        self.target_levels = parameter.declaration.target_levels
        self.required_level = parameter.declaration.required_level
        self.priority = parameter.declaration.priority
        self.allowed_reference_types = parameter.declaration.allowed_reference_types


    def parse_type_settings(self):
        """To be defined and called by the child classes in __init__"""
        raise NotImplementedError

    @staticmethod
    def factory(parameters):
        """
        Static method that takes a raw parameter statement, creates the
            proper object type and returns it

        Input : Raw parameter statement
        Output: BaseParameter child object of the type denoted int the
            parameter_declaration string

        TODO:
        """
        def match_subclass(parameter):
            parameter_type = parameter.declaration.parameter_type
            for cls in BaseParameter.__subclasses__():
                if parameter_type in cls.parameter_type:
                    return cls(parameter)
            raise TypeError("Bad parameter type: '{}'".format(parameter_type))

        if type(parameters) is str:
            parameters = [parameters]
        elif type(parameters) is list:
            pass
        else: raise TypeError("parameters argument must be either a str or list of strs")

        parameters = [BaseParameter.parse_parameter(parameter) for parameter in parameters]
        return [match_subclass(parameter) for parameter in parameters]


    @staticmethod
    def parse_parameter(parameter):
        """
        Static method that takes a raw parameter statement and parses
            it completely

        Input : parameter statement (string)
        Output: ParameterStatement Named Tuple
        """
        Parameter = namedtuple('Parameter',
                               ['declaration',
                                'type_settings'])

        #Return parameter ntuple if passed in to avoid double parsing 
        if type(parameter).__name__ is 'Parameter':
            return parameter

        split_statement = parameter.strip('`').split('`')
        if len(split_statement) != 2:
            raise SyntaxError("Parameter statements must have excatly two sections")

        declaration = BaseParameter.parse_parameter_declaration(split_statement[0])
        type_settings = re.split(',| ', split_statement[1])
        return Parameter(declaration=declaration,
                         type_settings=type_settings)

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

        #REMOVE the parameter type from the list 
        split_declaration.remove(tmp_parameter_dec.parameter_type)

        target_levels = []
        required_level = None
        priority = None
        allowed_file_references = []
        for declaration_setting in split_declaration:
            setting = BaseParameter.match_declaration_setting('Level', declaration_setting)
            if setting:
                target_levels.append(int(setting))
                continue

            setting = BaseParameter.match_declaration_setting('LevelRequired', declaration_setting)
            if setting:
                if required_level is None: required_level = int(setting)
                else: raise SyntaxError("There can only be ONE 'Required Level' set in a 'Parameter Declaration'")
                continue

            setting = BaseParameter.match_declaration_setting('Priority', declaration_setting)
            if setting:
                if priority is None: priority = int(setting)
                else: raise SyntaxError("There can only be ONE 'Priority' setting in a 'Parameter Declaration'")
                continue

            if declaration_setting in [ref for duo in BaseParameter.valid_file_references for ref in duo]:
                allowed_file_references.append(declaration_setting)
            else:
                raise TypeError("Error: Unknown parameter declaration setting: {}".format(declaration_setting))

        tmp_parameter_dec.target_levels = target_levels
        tmp_parameter_dec.required_level = required_level
        tmp_parameter_dec.priority = priority
        tmp_parameter_dec.allowed_file_references = allowed_file_references
        return tmp_parameter_dec

    @staticmethod
    def match_declaration_setting(declaration_setting_name, declaration_setting):
        """
        Input: Takes a declaration setting name to access data from,
            the string to look for the declaration setting name in
        Output: Returns the desired setting value if setting type is a
            match, returns None if nothing found
        """
        for name in BaseParameter.declaration_settings[declaration_setting_name].names:
            search = re.search(BaseParameter.declaration_settings[declaration_setting_name].regex_parse.format(name), declaration_setting)
            if search:
                return search.group(1)
        return ""

if __name__ == '__main__':
    ################# TESTING ##################

    # Data Reference parsing tests

    ## Parameter Factory Test: PASSED!
    ### Basic parameter: PASSED!
    parameter_type = "r"
    parameter_declaration = "`r`stuff`"
    #print(type(BaseParameter.factory(parameter_declaration)))

    ### Compound parameter PASSED!
    parameter_declaration = "`r-L1-L2-Lr3-P1`stuff`"
    ps = BaseParameter.factory(parameter_declaration)
    print(type(ps))
    [print(p.target_levels) for p in ps]
    [print(p.required_level) for p in ps]
    [print(p.priority) for p in ps]

    """
    ## Basic Full Data Reference Parsing:
    data_reference = "/data/string`r-L1-L2-Lr3-P1`stuff`"
    d = DataReference(data_reference)
    """

    # Full Data statement parsing tests

    # LASDI file path tests

    # LASDI Raw Data tests

    pass


