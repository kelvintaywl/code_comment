# -*- coding: utf-8 -*-

import os.path

from code_comment.models import Comment
from code_comment.errors import CodeLanguageUnsupported


class CodeLanguage:
    PYTHON = 'python'
    PHP = 'php'
    JAVASCRIPT = 'javascript'
    GOLANG = 'go'

    @staticmethod
    def factory(code_name):
        if code_name == CodeLanguage.PYTHON:
            return PythonCodeLanguage
        if code_name == CodeLanguage.PHP:
            return PHPCodeLanguage
        elif code_name == CodeLanguage.JAVASCRIPT:
            return JavascriptCodeLanguage
        elif code_name == CodeLanguage.GOLANG:
            return GolangCodeLanguage
        raise CodeLanguageUnsupported


class BaseCodeLanguage(CodeLanguage):

    # header, footer prefixes/suffixes
    SINGLE_LINE_COMMENT = ('//', None)
    # header, middle, footer prefixes/suffixes
    MULTI_LINE_COMMENT = ('/*', None, '*/')


class JavascriptCodeLanguage(BaseCodeLanguage):
    pass


class GolangCodeLanguage(BaseCodeLanguage):
    pass


class PHPCodeLanguage(BaseCodeLanguage):
    # NOTE: assuming PHPDoc style
    MULTI_LINE_COMMENT = ('/**', '*', '*/')


class PythonCodeLanguage(CodeLanguage):

    SINGLE_LINE_COMMENT = ('#', None)
    MULTI_LINE_COMMENT = ('"""', None, '"""')


class Parser:

    SUPPORTED_CODE_FILE_EXTENSIONS = {
        'py': CodeLanguage.PYTHON,
        'php': CodeLanguage.PHP,
        'js': CodeLanguage.JAVASCRIPT,
        'go': CodeLanguage.GOLANG
    }

    @staticmethod
    def is_supported_code_extension(ext):
        if not ext:
            return False
        return ext in Parser.SUPPORTED_CODE_FILE_EXTENSIONS

    @staticmethod
    def is_code_file(path):
        if not os.path.isfile(path):
            return False

        return Parser.is_supported_code_extension(
            os.path.splitext(path)[1][1:]  # ignore '.'
        )

    def __init__(self, filepath):
        self.filepath = filepath
        if not self.is_code_file(self.filepath):
            raise CodeLanguageUnsupported

        self.code_language = CodeLanguage.factory(
            self.determine_code_language()
        )

    def determine_code_language(self):
        ext = os.path.splitext(self.filepath)[1][1:]
        return self.SUPPORTED_CODE_FILE_EXTENSIONS.get(ext)

    def __iter__(self):
        return self.parse()

    def parse(self):
        c = self.code_language
        slc_header, slc_footer = c.SINGLE_LINE_COMMENT
        mlc_header, mlc_middle, mlc_footer = c.MULTI_LINE_COMMENT

        # to hold current mulitline comment info temporarily;
        # empty if parser not on multiline comment
        tmp = []

        def is_currently_multi_line_comment():
            return bool(tmp)

        def is_single_line_comment(text):
            return (
                not is_currently_multi_line_comment()
                and text.startswith(slc_header)
                and not slc_footer
            )

        def is_single_line_comment_multiline_notation(text):
            return (
                not is_currently_multi_line_comment()
                and text.startswith(mlc_header)
                and text.endswith(mlc_footer)
            )

        def is_multi_line_comment_start(text):
            return (
                not is_currently_multi_line_comment()
                and text.startswith(mlc_header)
                and not text.endswith(mlc_footer)
            )

        def is_multi_line_comment_midst(text):
            return (
                is_currently_multi_line_comment()
                and not text.startswith(mlc_header)
                and not text.endswith(mlc_footer)
                and (not mlc_middle or text.startswith(mlc_middle))
            )

        def is_multi_line_comment_end(text):
            return (
                is_currently_multi_line_comment()
                and text.endswith(mlc_footer)
            )

        with open(self.filepath, 'r') as f:
            for line_number, text in enumerate(
                [l.strip() for l in f], start=1
            ):
                if not text:
                    continue

                if is_single_line_comment(text):
                    comment_text = text.split(slc_header)[1].strip()
                    yield Comment(comment_text, self.filepath, line_number)

                elif is_single_line_comment_multiline_notation(text):
                    comment_text = text.split(mlc_header)[1]
                    comment_text = comment_text.rsplit(mlc_footer)[0].strip()
                    yield Comment(comment_text, self.filepath, line_number)

                elif is_multi_line_comment_start(text):
                    comment_text = text.split(mlc_header)[1].strip()
                    tmp.append([comment_text, line_number])

                elif is_multi_line_comment_midst(text):
                    comment_text = text
                    if mlc_middle:
                        comment_text = text.split(mlc_middle)[1].strip()
                    tmp.append([comment_text, line_number])

                elif is_multi_line_comment_end(text):
                    comment_text = text.rsplit(mlc_footer)[0].strip()
                    tmp.append([comment_text, line_number])
                    comment_texts, line_numbers = zip(*tmp)
                    tmp = []
                    yield Comment(
                        list(comment_texts),
                        self.filepath,
                        [line_numbers[0], line_numbers[-1]],
                        is_multiline=True
                    )
