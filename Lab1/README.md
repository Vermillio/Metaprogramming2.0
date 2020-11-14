# C# Formatter
____
This python console app formats C# code and saves the result wherever you want on hard drive (or overwrites existing file if output_path is not specified).

Works with files, directories, projects.
Supports Preprocessor, Generics, LINQ.

You can use default template.json formatting settings or add your own.
For description of specific setting go here: https://docs.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/formatting-rules
____
Usage: 
format.py [-h] --input_path INPUT_PATH [--output_path OUTPUT_PATH] (-f | -d | -p) -t TEMPLATE
