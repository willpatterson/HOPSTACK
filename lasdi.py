"""
Main file for the LASubway Data Interpreter (LASDI)

TODO:
    - Implement regex input string selection
    - Implement network file downloads
    - Implement file-path search on the "Metro Network" if a path is not found on file system
    - Implement local file path search within the metro directory **I now have doubts about this
"""

import os
import ntpath
import urllib

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

    elif os.path.isdir(data_string):
        #if is_metro(data_string): TODO Implement please
        #    return run_metro(data_string)  
        return extract_dir_files()

    #External Download interfaces TODO Implement Please
    elif data_string.startswith("ftp://"):
        raise NotImplementedError
    elif data_string.startswith("sftp://"):
        raise NotImplementedError
    elif data_string.startswith("http://") or data_string.startswith("https://"):
        raise NotImplementedError

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
            return data_interpreter(line, out_directory):

def extract_dir_files(dir_path, out_directory):
    """Opens a directory and returns a list of verified input strings"""

    for path in [os.path.join(dir_path, i) for i in os.listdir(dir_path)]:
        return data_interpreter(path, out_directory):

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

"""
****Replaced by extract_zip_file because of similarity with tar extraction****

class ZIPFile(CompressedFile):
    magic_signature = "\x50\x4b\x03\x04"
    filetype = "zip"
    default_extention = ".zip"

    def decompress(self):
        zip_name = ntpath.basename(self.path)
        un_zip_path = os.path.join(tar_file, tar_name)
        tar_file.TarFile(tar_file)
        tar_file.extractall(out_directory)

    return data_interpreter(un_tar_path, out_directory)


        return zipfile.ZipFile(self.path)
"""
