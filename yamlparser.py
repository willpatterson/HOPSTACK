"""
TODO:
    Turn read_yaml() into LASDO factory
    explore multiple yaml files per actual file
"""

import yaml
from collections import namedtuple

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
