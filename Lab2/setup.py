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
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library that provides ability to fix naming and comments in Kotlin code files according to Kotlin code conventions',
  author = 'Vermillio',     
  author_email = 'morganas.scream@gmail.com',     
  url = 'https://github.com/Vermillio/Metaprogramming2.0', 
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['code conventions', 'formatting', 'naming', 'Kotlin', 'C#', 'lexical analysis', 'parsing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)