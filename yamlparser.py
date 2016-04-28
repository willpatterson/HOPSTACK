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

    def format_command(self, unique_item=None):
        """
        Formats a command from the base command with class variables
        and adds them the the batches' command list
        """

        inserts = {}
        if '{exe}' in self.command_base:
            inserts["exe"] = self.executable
        if '{out}' in self.command_base:
            inserts["out"] = '{out}'
        if '{mod}' in self.command_base:
            inserts["mod"] = self.model_path

        if '{in}' in self.command_base:
            inserts["in"] = os.path.join(self.model_path, 'in')
        if '{unique}' in self.command_base:
            inserts["unique"] = unique_item

        if '{cpus}' in self.command_base:
            inserts["cpus"] = self.cpus

        self.commands.append(self.command_base.format(**inserts))


