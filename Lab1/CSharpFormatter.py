import os
import argparse
import fnmatch
        

class CSharpFormatter:

    def beautify(self, str, template=None):
        SyntaxTree = BuildAST(str)

        return str




if __name__ == "__main__":
    formatter = CSharpFormatter()

    parser = argparse.ArgumentParser(description="Specify input and output!")
    parser.add_argument("--input_path", help="path to format", required=True)
    parser.add_argument("--output_path", help="path to save result", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="file", action='store_true')
    group.add_argument("-d", "--directory", help="directory", action='store_true')
    group.add_argument("-p", "--project", help="project", action='store_true')

    parser.add_argument("--template", help="path to template file")
    args = parser.parse_args()

    template = None if not args.template else args.template

    if args.file:
        with open(args.input_path) as fi:
            str = fi.read()
            beautified_str = formatter.beautify(str, template)
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
        for dir, _, files in os.walk(args.input_path):
            rel_dir = os.path.relpath(dir, args.input_path)
            for file in fnmatch.filter(files, "*.cs"):
                rel_file = os.path.join(rel_dir, file)
                with open(os.path.join(dir, file)) as f:
                    str = f.read()
                    beautified_str = formatter.beautify(str, template)
                    out_file = os.path.join(args.output_path, rel_file)
                    if not os.path.exists(os.path.dirname(out_file)):
                        try:
                            os.makedirs(os.path.dirname(out_file))
                        except OSError as exc: # Guard against race condition
                            if exc.errno != errno.EEXIST:
                                raise
                    with open(out_file, 'w') as fo:
                        fo.write(beautified_str)
