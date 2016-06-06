"""
This is a general starting file for LASubway

TODO:
    Get the full path for Base dir in metro
"""

class LASDataObject(object):
    """
    Base object for all other LASDataObjects (metro, metro line, station)
    """
    def __init__(self, init_data):
        self.name = init_data['name']
        self.base_directory = init_data['base_dir']
        self.comments = init_data['comments']

    def export_diagram(self):
        """
        Returns a ascii table of the data object
        """
        raise NotImplementedError

    @staticmethod
    def create_box(width, title, body):
        """
        Creates a box with a title body and a specified width
        """
        pass #TODO Left off here


class Metro(LASDataObject):
    """
    """
    def __init__(self, init_data):
        super.__init__(self, init_data)
        self.required_pacakges = init_data['required_pacakges']

    def load_metro(self):
        pass


class Station(LASDataObject):
    """
    """
    def __init__(self, init_data):
        super.__init__(self, init_data)
        self.in_stream = init_data['in']   #TODO Consider multiple streams for one station
        self.out_stream = init_data['out'] #
        self.cmd = init_data['cmd']

class Box(object):

    def __init__(self, width, title, body):
        self.box_lines = []
        self.width = width
        self.title = title
        self.body = body

        boxend = '+{}+'.format(repeat_char('-', self.width-2))
        self.box_lines.append(boxend)
        self.box_lines = self.box_lines + self.format_box_string(title)
        self.box_lines.append('+{}+'.format(repeat_char('=', width-2)))
        self.box_lines = self.box_lines + self.format_box_string(body)
        self.box_lines.append(boxend)

    def print_box(self):
        for line in self.box_lines:
            print(line)

    def box_to_string(self):
        return '\n'.join(self.box_lines)

    def format_box_string(self, string):
        box_lines = []
        while len(string) > self.width-2:
            try:
                line = self.format_box_line(string[:self.width-2])
                string = string[(self.width-2):]
            except IndexError:
                line = self.format_box_line(string)
            box_lines.append(line)

        box_lines.append(self.format_box_line(string))
        return box_lines

    def format_box_line(self, string):
        return '|{}{}|'.format(string, repeat_char(' ', self.width-len(string)-2))

def repeat_char(char, ntimes):
    """returns a string of chars repeated ntimes"""
    s = ""
    for i in range(ntimes):
        s += char
    return s


if __name__ == '__main__':
    width = 20
    title = "tsty testy testasdfasdfasd asdfjkdsfkljasdf"
    body = "How about this box formatting? Its looking pretty decient RN. I hope it translates into good stuff"
    tbox = Box(width, title, body)
    tbox.print_box()
