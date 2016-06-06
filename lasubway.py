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
    """ASCII box drawing class"""

    def __init__(self, width, title, body):
        """Sets up class variables and creates box"""

        self.box_lines = []
        self.width = width
        self.title = title
        self.body = body

        boxend = '+{}+'.format(self.repeat_char('-', self.width-2))
        self.box_lines.append(boxend)
        self.format_box_string(title) #Add title
        self.box_lines.append('+{}+'.format(self.repeat_char('=', width-2)))
        self.format_box_string(body)  #Add body
        self.box_lines.append(boxend)

    def print_box(self):
        """Prints box"""
        for line in self.box_lines:
            print(line)

    def box_to_string(self):
        """Returns box as one string"""
        return '\n'.join(self.box_lines)

    def format_box_string(self, string):
        """adds a multiline string to the box"""

        string.lstrip() #Remove begining whitespace
        while len(string) > self.width-2:
            try:
                self.format_box_line(string[:self.width-2])
                string = string[(self.width-2):].lstrip()
            except IndexError:
                self.format_box_line(string)
        self.format_box_line(string)

    def format_box_line(self, string):
        """Adds one line to the box"""
        self.box_lines.append('|{}{}|'.format(string, self.repeat_char(' ', self.width-len(string)-2)))

    def resize_width(self, new_width):
        """"""
        raise NotImplementedError

    @staticmethod
    def repeat_char(char, ntimes):
        """returns a string of chars repeated ntimes"""
        s = ""
        for i in range(ntimes):
            s += char
        return s

class Structure(object):
    """A box that can contain mulitple boxes"""

    def __init__(self, width, title, body):
        pass



if __name__ == '__main__':
    width = 20
    title = "tsty testy testasdfasdfasd asdfjkdsfkljasdf"
    body = "How about this box formatting? Its looking pretty decient RN. I hope it translates into good stuff"
    tbox = Box(width, title, body)
    tbox.print_box()
