
class DownloadError(Exception):
    """
    To be raised when a connection
    to the source puzzle server fails
    """
    pass


class ParseError(Exception):
    """
    To be raised when parsing of a
    puzzle response fails
    """
    pass
