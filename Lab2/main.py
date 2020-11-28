from Lab2.KotlinStyleChecker import KotlinStyleChecker

def fixup_code_style(input_path):
    kotlin_style_checker = KotlinStyleChecker()
    file_contents = []
    for dir, _, files in os.walk(args.input_path):
        rel_dir = os.path.relpath(dir, args.input_path)
        kotlin_files = fnmatch.filter(files, "*.kt")
        for file in kotlin_files:
            rel_file = os.path.join(rel_dir, file)
            print("Processing file " + rel_file)
            with open(os.path.join(dir, file)) as f:
                file_contents.append(f.read())
    kotlin_style_checker.fix(file_contents, log_file=os.path.join(dir, file)[:-3]+"_fixing.log")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify input")
    parser.add_argument("--input_path", help="project or file path, will be overwritten", required=True)
    args = parser.parse_args()

fixed_str = ""

with open('Lab2/input.txt') as f:
    str = f.read()
    kotlin_style_checker = KotlinStyleChecker()
    fixed_str = kotlin_style_checker.fix(str, log_file="output.log")

print(fixed_str)
