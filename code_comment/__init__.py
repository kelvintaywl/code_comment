# -*- coding: utf-8 -*-
"""
    Code Comment
    ~~~~~~
    Code Comment is a library to extract code comments from source codes.
"""

from code_comment.models import Comment
from code_comment.lib import Parser


def extract(filepath):
    return Parser(filepath)


__all__ = ['Comment', 'extract']
