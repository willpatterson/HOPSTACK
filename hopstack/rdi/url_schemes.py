#Scheme classes are proably an unessary abstraction. Should use functions instead
#TODO: Change scheme classes to functions
class Scheme(object):
    """
    Defines the base class for classes used by DataInterpreter to access
    data remotely
    """
    scheme_names = []
    def __init__(self):
        pass

    @classmethod
    def is_scheme(cls, in_scheme):
        return in_scheme in cls.scheme_names

class HttpsScheme(Scheme):
    scheme_names = ['http','https']

class FtpScheme(Scheme):
    scheme_names = ['ftp'] #maybe SFTP too

class SshScheme(Scheme):
    scheme_names = ['ssh']

class FileScheme(Scheme):
    scheme_names = ['file']

    def extract_sin_files(sin_path):
        """
        Opens a Station Input File and returns a list of verified input strings
        (A Station file contains filepaths to other files. extention: .sin)
        """

        in_strings = []
        with open(sin_path, 'r') as sinfile:
            for line in sinfile:
                yield line

    def extract_dir_files(dir_path):
        """
        Opens a directory and returns a list of verified input strings
        """

        for path in [os.path.join(dir_path, i) for i in os.listdir(dir_path)]:
            yield path

    def extract_tar_files(tar_file):
        """
        extracts all files in a tar archive
        TODO: THIS IS BROKEN
        tar_name = ntpath.basename(tar_file)
        un_tar_path = os.path.join(tar_file, tar_name)
        tarfile.TarFile(tar_file)
        tarfile.extractall(out_directory)

        return un_tar_path
        """
        pass

    def extract_zip_files(zip_file):
        """
        extracts all files in a zip archive
        TODO: THIS IS BROKEN
        zip_name = ntpath.basename(zip_file)
        un_zip_path = os.path.join(zip_file, zip_name)
        zipfile.TarFile(zip_file)
        zipfile.extractall(out_directory)

        return un_zip_path
        """
        pass

    def extract_compresson_file(compression_file):
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
        Attempts to detect compression type
        The code used was found at:
        http://stackoverflow.com/questions/13044562/python-mechanism-to-identify-compressed-file-type-and-uncompress
        """
        with file(filename, 'rb') as f:
            start_of_file = f.read(1024)
            f.seek(0)
            for cls in (BZ2File, GZFile):
                if cls.is_magic(start_of_file):
                    return cls(f)

            return None

class WorkSpaceScheme(Scheme):
    scheme_names = ['workspace']


