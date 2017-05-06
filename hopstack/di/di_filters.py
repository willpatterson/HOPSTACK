
class RegexFilter(BaseParameter):
    """
    Parameter object that filters strings with a python regex
    TODO:
        support escape sequence for '`'
    """
    parameter_type = ('ref', 'regex_filter')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RegexSubstring(BaseParameter):
    """
    """
    parameter_type = ('res', 'regex_sub')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """ """
        raise NotImplementedError

class ExentionFilter(BaseParameter):
    """Parameter object that filters verified file paths by extention"""
    parameter_type = ('e', 'extention')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class SubstringFilter(BaseParameter):
    """
    Parameter object that filters all strings by substring inclusion
    """
    parameter_type = ('s', 'substring')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RangeFilter(BaseParameter):
    """
    Parameter object that filters out all files not in the specified range
    """
    parameter_type = ('r', 'range')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RequiredRangeFilter(BaseParameter):
    """
    Parameter object that filters out all files not in the specified
    range but will throw error if not all number in range found
    """
    parameter_type = ('rr', 'required_range')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class SinFileParameter(BaseParameter):
    """Takes in a sin file, returns its contents iteratively"""
    parameter_type = ('sin', 'station_in')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class RawDelimiter(BaseParameter):
    """
    Parameter object that opens files and returns chuncks of delimited text
    """
    parameter_type = ('rd', 'raw_dilimeter')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class TargetLevels(BaseParameter):
    """Parameter object that dictates operations on a target level"""
    parameter_type = ('tl', 'target_levels')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError

class HyperlinkFilter(BaseParameter):
    """
    Parameter object that searches for and returns hyperlinks
    on webpages
    """
    parameter_type = ('h', 'hyperlink')
    def __init__(self, parameter_declaration):
        super().__init__(parameter_declaration)

    def parse_type_settings(self):
        """"""
        raise NotImplementedError


