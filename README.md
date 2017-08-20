# Code Comment

Parser to extract code comments in source codes.

> Requires Python 3

## Supported Languages

- Go
- Javascript
- PHP
- Python

## Example Usage

```python

import code_comment

for comment in code_comment.extract(filepath):
    # isinstance(comment, code_comment.Comment) == True
    print(str(comment))
    print(comment.line_number_str)  # e.g.
    print(comment.body_str)  # e.g.
    print(comment.filepath)  # e.g. 

```
