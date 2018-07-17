# -*- coding: utf-8 -*-

import os.path
import re

from code_comment.models import Comment
from code_comment.errors import CodeLanguageUnsupported


class CodeLanguage:
    PYTHON = 'python'
    PHP = 'php'
    JAVASCRIPT = 'javascript'
    GOLANG = 'go'
    CPP = 'cpp'
    C = 'c'
    JAVA = 'java'
    H = 'h'
    CSS = 'css'
    HTML = 'html'

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
        elif code_name == CodeLanguage.CPP:
            return CppCodeLanguage
        elif code_name == CodeLanguage.C:
            return CCodeLanguage
        elif code_name == CodeLanguage.JAVA:
            return JavaCodeLanguage
        elif code_name == CodeLanguage.H:
            return CppHeaderCodeLanguage
        elif code_name == CodeLanguage.CSS:
            return CSSCodeLanguage
        elif code_name == CodeLanguage.HTML:
            return HTMLCodeLanguage
        raise CodeLanguageUnsupported


class BaseCodeLanguage(CodeLanguage):

    # header, footer prefixes/suffixes
    SINGLE_LINE_COMMENT = ('//', None)
    # header, middle, footer prefixes/suffixes
    MULTI_LINE_COMMENT = ('/*', None, '*/')


class JavascriptCodeLanguage(BaseCodeLanguage):
    pass

class CSSCodeLanguage(BaseCodeLanguage):
    pass

class GolangCodeLanguage(BaseCodeLanguage):
    pass

class CppCodeLanguage(BaseCodeLanguage):
    pass

class CCodeLanguage(BaseCodeLanguage):
    pass

class JavaCodeLanguage(BaseCodeLanguage):
    pass

class CppHeaderCodeLanguage(BaseCodeLanguage):
    pass

class PHPCodeLanguage(BaseCodeLanguage):
    # NOTE: assuming PHPDoc style
    MULTI_LINE_COMMENT = ('/*', None, '*/')

class HTMLCodeLanguage(BaseCodeLanguage):
    MULTI_LINE_COMMENT = ('<!--', None, '-->')

class PythonCodeLanguage(CodeLanguage):

    SINGLE_LINE_COMMENT = ('#', None)
    MULTI_LINE_COMMENT = ('"""', None, '"""')




class Parser:

    SUPPORTED_CODE_FILE_EXTENSIONS = {
        'py': CodeLanguage.PYTHON,
        'php': CodeLanguage.PHP,
        'js': CodeLanguage.JAVASCRIPT,
        'go': CodeLanguage.GOLANG,
        'cpp': CodeLanguage.CPP,
        'cc': CodeLanguage.CPP,
        'c': CodeLanguage.C,
        'java': CodeLanguage.JAVA,
        'h': CodeLanguage.H,
        'hpp': CodeLanguage.H,
        'css': CodeLanguage.CSS,
        'html': CodeLanguage.HTML
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

        def is_python():
            return self.determine_code_language() == 'python'

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
                and len(text) >= 6
            )

        def is_multi_line_comment_start(text):
            return (
                not is_currently_multi_line_comment()
                and text.startswith(mlc_header)
                and (not text.endswith(mlc_footer) or len(text) == 3)
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
        
        def is_multi_line_print_starts(text):
            return (
                is_python() 
                and re.search(r'(?!^)"""', text, re.M)
            )

        def is_multi_line_print_in_single_line(text):
            return (
                is_python() 
                and len(re.findall(r'(?!^)"""', text, re.M)) >= 2
            )
        
        flag = 0
        with open(self.filepath, 'r') as f:
            for line_number, text in enumerate(
                [l.strip() for l in f], start=1
            ):
                text = re.sub(r"'''", '"""', text)
                # print(text)
                # if multi line print starts and python then continue 
                # if multi print is going on 
                # if multi stops then look from next line 

                
                # is_multi_line_print_in_python(text)
                # print("code language is ", self.determine_code_language())
                # print("Log1", text)
                # aaa = is_multi_line_comment_midst(text)
                # print("Log2",aaa)

                # print("is_single_line_comment.    ", is_single_line_comment(text))
                # print("is_single_line_comment_multiline_notation.   ", is_single_line_comment_multiline_notation(text))
                # print("is_multi_line_comment_start(text).    ", is_multi_line_comment_start(text))
                # print("is_multi_line_comment_midst   ",aaa)
                # print("is_multi_line_comment_end    ", is_multi_line_comment_end(text))
                if not text:
                    continue

                if is_multi_line_print_in_single_line(text):
                    # Start and End of Multiline python comment in Single line
                    flag = 0
                    continue

                elif is_multi_line_print_starts(text) and flag == 0:
                    # Multi line print starts
                    flag = 1
                    continue

                elif is_python() and flag == 1 and re.search(r'"""', text):
                    # Multi line print ends
                    flag = 0
                    continue

                elif is_python() and flag == 1:
                    # Multi line print continues
                    continue

                elif is_single_line_comment(text):
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
