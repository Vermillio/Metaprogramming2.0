from CSharpFormatter import *
from tests import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify input and output!")
    parser.add_argument("--input_path", help="path to format", required=True)
    parser.add_argument("--output_path", help="path to save result", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="file", action='store_true')
    group.add_argument("-d", "--directory", help="directory", action='store_true')
    group.add_argument("-p", "--project", help="project", action='store_true')

    parser.add_argument("--template", help="path to template file")
    args = parser.parse_args()

    template_path = None if not args.template else args.template
    template = parse_template(template_path)

    if run_tests() < 0.9:
        print("Many tests failed. Operation stopped. See errors.log")
    else:
        with open('errors.log', 'w+') as errors_log_file:
            if args.file:
                with open(args.input_path) as fi:
                    errors_log_file.write("Processing file " + args.input_path)
                    str = fi.read()
                    beautified_str = CSharpFormatter().beautify(str)
                    out_file = args.output_path
                    if not os.path.exists(os.path.dirname(out_file)):
                        try:
                            os.makedirs(os.path.dirname(out_file))
                        except OSError as exc: # Guard against race condition
                            if exc.errno != errno.EEXIST:
                                raise
                    with open(out_file, 'w') as fo:
                        fo.write(beautified_str)
            elif args.directory:
                print("Processing directory " + args.input_path)
                for dir, _, files in os.walk(args.input_path):
                    rel_dir = os.path.relpath(dir, args.input_path)
                    for file in fnmatch.filter(files, "*.cs"):
                        rel_file = os.path.join(rel_dir, file)
                        print("Processing file " + rel_file)
                        errors_log_file.write("Processing file " + rel_file)
                        with open(os.path.join(dir, file)) as f:
                            str = f.read()
                            print(ord(str[0]))
                            beautified_str = CSharpFormatter().beautify(str)
                            out_file = os.path.join(args.output_path, rel_file)
                            print("Writed string to file")
                            if not os.path.exists(os.path.dirname(out_file)):
                                try:
                                    os.makedirs(os.path.dirname(out_file))
                                except OSError as exc: # Guard against race condition
                                    if exc.errno != errno.EEXIST:
                                        raise
                            with open(out_file, 'w') as fo:
                                fo.write(beautified_str)
                                print("Writed string to file")
