import os
import argparse
import fnmatch
from Lab2.KotlinStyleChecker import KotlinStyleChecker
from Lab2.KotlinLexer import KotlinLexer

def fixup_code_style(input_path):
    kotlin_style_checker = KotlinStyleChecker()
    file_contents = []
    file_names = []
    for dir, _, files in os.walk(input_path):
        rel_dir = os.path.relpath(dir, input_path)
        kotlin_files = fnmatch.filter(files, "*.kt")
        for file in kotlin_files:
            print("Processing file " + os.path.join(rel_dir, file))
            file_name = os.path.join(dir, file)
            with open(file_name) as f:
                file_contents.append(f.read())
                file_names.append(file_name)
    file_contents = kotlin_style_checker.fix(file_contents, log_files=[f[:-3]+"_fixing.log" for f in file_names])
    for file_name,  file_content in zip(file_names, file_contents):
        with open(file_name, 'w') as f:
            f.write(file_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify input")
    parser.add_argument("--input_path", help="project or file path, will be overwritten", required=True)
    args = parser.parse_args()
