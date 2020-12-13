from distutils.core import setup
import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('py2sqlite3/py2sqlite3.py').read(),
    re.M
).group(1)

setup(
  name = 'py2sqlite3',
  packages=setuptools.find_packages(),
  version = version,
  license='MIT',
  description = 'py2sqlite3 is a library that facilitates the communication between python objects and sqlite3 databases.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Vermillio',
  author_email = 'morganas.scream@gmail.com',
  url = 'https://github.com/Vermillio/Metaprogramming2.0',
  download_url = 'https://github.com/Vermillio/Metaprogramming2.0/archive/alpha.zip',
  keywords = ['orm', 'sql', 'sqlite3', '', 'C#', 'lexical analysis', 'parsing'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  python_requires='>=3.6',
)
