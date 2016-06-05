"""
This is a general starting file for LASubway
This file was formally used to start LASDI
"""

class LASDataObject(object):
    """
    Base object for all other LASDataObjects (metro, metro line, station)
    """
    def __init__(self, init_data):
        self.name = init_data['name']
        self.base_directory = init_data['base_dir']
        self.comments = init_data['comments']

class Metro(LASDataObject):
    """
    """
    def __init__(self, init_data):
        super.__init__(self, init_data)
        self.required_pacakges = init_data['required_pacakges']


class Station(LASDataObject):
    """
    """
    def __init__(self, init_data):
        super.__init__(self, init_data)
        self.in_stream = init_data['in']   #TODO Consider multiple streams for one station
        self.out_stream = init_data['out'] #
        self.cmd = init_data['cmd']




