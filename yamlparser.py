class YamlFile:
    def __init__(self, yaml_path):
        pass

class Metro:
    def __init__(self, metro_file):
        base_dir = None


class Station:
    def __init__(self, station_data):
       self.name = station_data["name"]
       self.

def format_command(replace_items, command):
    """
    """

    inserts = {}
    for key, item in replace_items.itmes():
        if '\{{}\}'.format(key) in command: #TODO: Revise this. 
            inserts[key] = item             # Ask for forgiveness or permission?
        else:                               #
            print('Warning, item not found')#

    return command_base.format(**inserts)


