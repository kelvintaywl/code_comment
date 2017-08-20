# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


VERSION = '0.1.0'
REPO_URL = 'https://github.com/kelvintaywl/code_comment'

requires = []

extras_require = {
    "test": [
        "pytest",
        "pytest-cov",
        "flake8"
    ]
}

setup(name='code_comment',
      version=VERSION,
      description='extracts code comments from source codes',
      author='Kelvin Tay',
      author_email='kelvintay@gmail.com',
      url=REPO_URL,
      download_url='{}/tarball/{}'.format(REPO_URL, VERSION),
      keywords='comment, extract',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require=extras_require)
