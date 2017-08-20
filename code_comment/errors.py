# -*- coding: utf-8 -*-


class CommentNotTerminated(Exception):
    """ Error when detected comment was not terminate cleanly. """
    pass


class CodeLanguageUnsupported(Exception):
    """ Error when detected code language is not supported. """
    pass
