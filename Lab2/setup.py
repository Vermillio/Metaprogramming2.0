from distutils.core import setup
import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('kotlin_style_check/KotlinStyleChecker.py').read(),
    re.M
).group(1)

setup(
  name = 'kotlin_style_check',       
  packages=setuptools.find_packages(),
  version = version,     
  license='MIT',  
  description = 'Library that provides ability to fix naming and comments in Kotlin code files according to Kotlin code conventions',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Vermillio',     
  author_email = 'morganas.scream@gmail.com',     
  url = 'https://github.com/Vermillio/Metaprogramming2.0',
  keywords = ['code conventions', 'formatting', 'naming', 'Kotlin', 'C#', 'lexical analysis', 'parsing'],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',   
    'License :: OSI Approved :: MIT License',
  ],
  python_requires='>=3.6',
)