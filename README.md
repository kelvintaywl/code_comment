# Code Comment
[![Build Status](https://travis-ci.org/kelvintaywl/code_comment.svg?branch=master)](https://travis-ci.org/kelvintaywl/code_comment)

Parser to extract code comments in source codes.

> Requires Python 3.3+

## Supported Languages

- Go
- Javascript
- PHP
- Python
- CPP
- C
- JAVA

## Example Usage

### Example file (`dummy.py`)
```python
""" Dummy
Lorem Ipsum
"""


def main():
    # nothing to see here!
    # しかし、日本語でも大丈夫だよ！
    print('Hello Python')


if __name__ == '__main__':
    """ Test single-line multiline comment """
    main()

```

```python

import code_comment

filepath = 'dummy.py'

for comment in code_comment.extract(filepath):
    do_something_with_comment(comment)

comments = list(code_comment.extract(filepath))
assert len(comments) == 4

first_comment = comments[0]
assert first_comment.is_multiline
assert first_comment.line_number_str = '1~3'
assert first_comment.filepath = 'dummy.py'
assert first_comment.body_str = 'Dummy\nLorem Ipsum\n'

print(str(first_comment))
# [dummy.py:1~3]   Dummy
# Lorem Ipsum

```
