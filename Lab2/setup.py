from distutils.core import setup
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('kotlin_style_check/KotlinStyleChecker.py').read(),
    re.M
).group(1)

setup(
  name = 'kotlin_style_check',       
  packages = ['kotlin_style_check'],   
  version = version,     
  license='MIT',  
  description = 'Library that provides ability to fix naming and comments in Kotlin code files according to Kotlin code conventions',
  author = 'Vermillio',     
  author_email = 'morganas.scream@gmail.com',     
  url = 'https://github.com/Vermillio/Metaprogramming2.0', 
  download_url = 'https://github.com/Vermillio/Metaprogramming2.0/archive/alpha.zip',
  keywords = ['code conventions', 'formatting', 'naming', 'Kotlin', 'C#', 'lexical analysis', 'parsing'],
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
)