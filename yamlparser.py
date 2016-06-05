"""

"""

import yaml
from collections import namedtuple

class LASDataObject(object):
    """
    """
    def __init__(self, init_data):
        name = init_data['name']
        base_directory = init_data['base_dir']
        comments = init_data['comments']

class Metro(LASDataObject):
    """
    """
    def __init__(self, init_data):
        super.__init__(self, init_data)
        required_pacakges = init_data['required_pacakges']

class Station(LASDataObject):
    """
    """
    def __init__(self, init_data):
        super.__init__(self, init_data)
        in_stream = init_data['in']
        out_stream = init_data['out']

def read_yaml(yaml_path):
    """
    Reads YAML file and yields its objects
    """
    YmlObj = namedtuple('YmlObj', ['name', 'data'])

    with open(yaml_path, 'r') as yfile:
        raw_yaml_data = yaml.load(yfile)

    print(raw_yaml_data)
    for yobj in raw_yaml_data:
        #yield YmlObj(name=yobj, data=yobj[
        print(yobj.keys())
        yield yobj


if __name__ == '__main__':
    yaml_path = './test/yaml_reader_test.yml'
    for i in read_yaml(yaml_path):
        pass 
