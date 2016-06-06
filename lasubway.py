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

def create_box(width, title, body):
    box_lines = []

    boxend = '+{}+'.format(repeat_char('-', width-2))
    box_lines.append(boxend)
    box_lines = box_lines + format_box_string(width, title)
    box_lines.append('+{}+'.format(repeat_char('=', width-2)))
    box_lines = box_lines + format_box_string(width, body)
    box_lines.append(boxend)


    return box_lines

def print_box(box):
    for line in box:
        print(line)

def box_to_string(box):
    return '\n'.join(box)

def repeat_char(char, ntimes):
    """returns a string of chars repeated ntimes"""
    s = ""
    for i in range(ntimes):
        s += char
    return s

def format_box_string(width, string):
    box_lines = []
    while len(string) > width-2:
        try:
            line = '|{}|'.format(string[:width-2])
            string = string[(width-2):]
        except IndexError:
            line = '|{}{}|'.format(string, repeat_char(' ', width-len(string)-2))
        box_lines.append(line)

    box_lines.append('|{}{}|'.format(string, repeat_char(' ', width-len(string)-2)))
    return box_lines

def format_box_line(width, string):
    return '|{}{}|'.format(string, repeat_char(' ', width-len(string)-2))

if __name__ == '__main__':
    width = 20
    title = "tsty testy testasdfasdfasd asdfjkdsfkljasdf"
    body = "How about this box formatting? Its looking pretty decient RN. I hope it translates into good stuff"
    print_box(create_box(width,title,body))
