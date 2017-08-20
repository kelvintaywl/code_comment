# -*- coding: utf-8 -*-
import os.path

import pytest

from code_comment.lib import (
    CodeLanguage,
    PythonCodeLanguage,
    PHPCodeLanguage,
    GolangCodeLanguage,
    JavascriptCodeLanguage,
    Parser
)
from code_comment.errors import CodeLanguageUnsupported


CURDIR = os.path.dirname(os.path.realpath(__file__))
FIXTURE_DIR = os.path.join(CURDIR, 'fixtures')


def test_code_language_factory_success():
    for language, KodeLanguage in [
        ('go', GolangCodeLanguage),
        ('javascript', JavascriptCodeLanguage),
        ('php', PHPCodeLanguage),
        ('python', PythonCodeLanguage)
    ]:
        klass = CodeLanguage.factory(language)
        assert klass == KodeLanguage


def test_code_language_factory_fail():
    with pytest.raises(CodeLanguageUnsupported):
        CodeLanguage.factory('unknown')


def test_parser_is_supported_code_extension_success():
    for ext in [
        'php', 'py', 'go', 'js'
    ]:
        assert Parser.is_supported_code_extension(ext) is True


def test_parser_is_supported_code_extension_fail():
    for ext in [
        '', None, 'cpp', 'rb'
    ]:
        assert Parser.is_supported_code_extension(ext) is False


def test_parser_init_fail():
    for unsupported_filepath in [
        os.path.join(FIXTURE_DIR, ''),
        os.path.join(FIXTURE_DIR, 'dummy.rb'),
    ]:
        with pytest.raises(CodeLanguageUnsupported):
            Parser(unsupported_filepath)


def test_parser_parse_python_success():
    parser = Parser(os.path.join(FIXTURE_DIR, 'dummy.py'))
    comments = list(parser)

    assert len(comments) == 4

    assert comments[0].line_number_str == '1~3'
    assert comments[0].is_multiline
    assert comments[0].body_str == 'Dummy\nLorem Ipsum\n'

    assert comments[1].line_number_str == '7'
    assert not comments[1].is_multiline
    assert comments[1].body_str == 'nothing to see here!'

    assert comments[2].line_number_str == '8'
    assert not comments[2].is_multiline
    assert comments[2].body_str == 'しかし、日本語でも大丈夫だよ！'

    assert comments[3].line_number_str == '13'
    assert not comments[3].is_multiline
    assert comments[3].body_str == 'Test single-line multiline comment'
