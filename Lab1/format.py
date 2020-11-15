from CSharpFormatter import *
from tests import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify input and output!")
    parser.add_argument("--input_path", help="path to format", required=True)
    parser.add_argument("--output_path", help="path to save result", required=False)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="file", action='store_true')
    group.add_argument("-d", "--directory", help="directory", action='store_true')
    group.add_argument("-p", "--project", help="project", action='store_true')

    parser.add_argument("-t", "--template", help="path to formatting settings .json", required=True)

    args = parser.parse_args()
    if args.template:
        Settings.parse_template(args.template)

    if run_tests() < 1.0:
        print("Some tests failed. Operation stopped. See errors.log")
    else:
        with open('errors.log', 'w+') as errors_log_file:
            if args.file:
                beautified_str = None
                with open(args.input_path) as fi:
                    print("Processing file " + args.input_path+'\n')
                    errors_log_file.write("Processing file " + args.input_path+'\n')
                    str = fi.read()
                    beautified_str = CSharpFormatter().beautify(str)
                if beautified_str!=None:
                    with open(args.output_path if args.output_path else args.input_path, 'w') as fo:
                        fo.write(beautified_str)
                    print("Completed.\n\n")
            elif args.directory or args.project:
                print("\nProcessing directory " + args.input_path+'\n')
                for dir, _, files in os.walk(args.input_path):
                    rel_dir = os.path.relpath(dir, args.input_path)
                    csharp_files = fnmatch.filter(files, "*.cs")

                    if args.project and args.output_path and args.output_path != args.input_path:
                        other_files = list(set(files) - set(csharp_files))
                        for file in other_files:
                            rel_file = os.path.join(rel_dir, file)
                            print("Copying file " + rel_file)
                            str = None
                            with open(os.path.join(dir, file)) as f:
                                str = f.read()
                            out_file = os.path.join(args.output_path, rel_file)
                            if not os.path.exists(os.path.dirname(out_file)):
                                try:
                                    os.makedirs(os.path.dirname(out_file))
                                except OSError as exc: # Guard against race condition
                                    if exc.errno != errno.EEXIST:
                                        raise
                            if str != None:
                                with open(out_file, 'w') as fo:
                                    fo.write(str)
                            print("Completed.\n\n")

                    for file in csharp_files:
                        rel_file = os.path.join(rel_dir, file)
                        print("Processing file " + rel_file)
                        errors_log_file.write("Processing file " + rel_file+'\n')
                        beautified_str = None
                        with open(os.path.join(dir, file)) as f:
                            str = f.read()
                            beautified_str = CSharpFormatter().beautify(str)

                        if beautified_str!=None:
                            out_file = os.path.join(args.output_path if args.output_path else args.input_path, rel_file)
                            if not os.path.exists(os.path.dirname(out_file)):
                                try:
                                    os.makedirs(os.path.dirname(out_file))
                                except OSError as exc: # Guard against race condition
                                    if exc.errno != errno.EEXIST:
                                        raise
                            with open(out_file, 'w') as fo:
                                fo.write(beautified_str)
                        print("Completed.\n\n")
    print("Completed.")
