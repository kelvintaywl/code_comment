# -*- coding: utf-8 -*-

from code_comment.models import Comment


def test_simple_comment_properties():
    comment = Comment('loren ipsum', '/tmp/test.js', 1)
    assert comment.body_str == 'loren ipsum'
    assert comment.line_number_str == '1'
    assert comment.filepath == '/tmp/test.js'
    assert not comment.is_multiline
    assert str(comment) == '[/tmp/test.js:1]\tloren ipsum'


def test_multiline_comment_properties():
    comment = Comment(
        ['line1', 'line2', 'line3'],
        '/tmp/test.js',
        [2, 4],
        is_multiline=True
    )
    assert comment.body_str == 'line1\nline2\nline3'
    assert comment.line_number_str == '2~4'
    assert comment.filepath == '/tmp/test.js'
    assert comment.is_multiline
    assert str(comment) == '[/tmp/test.js:2~4]\tline1\nline2\nline3'
