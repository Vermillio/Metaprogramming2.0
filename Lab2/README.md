# Kotlin Style Check
____

This open-source python package automatically fixes your Kotlin code to follow coding conventions listed here:

https://kotlinlang.org/docs/reference/coding-conventions.html#naming-rules

https://kotlinlang.org/docs/reference/coding-conventions.html#documentation-comments

____
## Installation

  https://pypi.org/project/kotlin-style-check/

  `pip install kotlin_style_check`
____

## RECOMMENDED: Usage from command line: 

  Searches for all .kt files in given path and fixes naming and comments errors

  `python -m kotlin_style_check --input_path`

____

## Usage as library (generally not recommended for casual users, but you can try):

### Example
```
from kotlin_style_check import KotlinStyleChecker

print(KotlinStyleChecker().fix(["val My_Var = 5;"], ["out.log"])) # outputs "val myVar = 5;", logs changes to "out.log"
```

#### Short description of class KotlinStyleChecker

```python def fix(self, file_contents, log_files) # file_contents - list of strings (connected files) to fix code style, log_files - list of log files for each item in file_contents

def fix_in_files(self, input_path) # input_path - path to dir or file to fix code style. logs data relatively to this path

def run_tests(self, log_file) # runs small checks

def setup_logger(self, log_file, level=logging.INFO) # needed to log data when calling lower level functions of this class (check_comments for example), overwrites it's global logger

""" ... other stuff you can find in source code """
```

