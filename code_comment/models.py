# -*- coding: utf-8 -*-


class Comment:

    def __init__(self, body, filepath, line_number, is_multiline=False):

        self._body = body
        self.filepath = filepath
        self._line_number = line_number
        self.is_multiline = is_multiline

    @property
    def line_number_str(self):
        if isinstance(self._line_number, list):
            return '{}~{}'.format(*self._line_number)

        return str(self._line_number)

    @property
    def body_str(self):
        if isinstance(self._body, list):
            return '\n'.join(self._body)

        return self._body

    def __str__(self):
        return '[{0.filepath}:{0.line_number_str}]\t{0.body_str}'.format(self)
