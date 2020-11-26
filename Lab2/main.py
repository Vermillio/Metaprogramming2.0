import KotlinStyleChecker from KotlinStyleChecker

def fixup_code_style(input_path):
    kotln_style_checker = KotlinStyleChecker()
    for dir, _, files in os.walk(args.input_path):
        rel_dir = os.path.relpath(dir, args.input_path)
        kotlin_files = fnmatch.filter(files, "*.kt")
        for file in kotlin_files:
            rel_file = os.path.join(rel_dir, file)
            print("Processing file " + rel_file)
            with open(os.path.join(dir, file)) as f:
                str = f.read()
                koltin_style_checker.fix(str, log_file=os.path.join(dir, file)[:-3]+"_fixing.log")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify input and output!")
