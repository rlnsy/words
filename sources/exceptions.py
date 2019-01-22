class SourceError(Exception):
    """
    To be raised when a puzzle source fails
    for some reason
    """
    pass


class DownloadError(SourceError):
    """
    To be raised when a connection
    to the source puzzle server fails
    """
    pass


class ParseError(SourceError):
    """
    To be raised when parsing of a
    puzzle response fails
    """
    pass
