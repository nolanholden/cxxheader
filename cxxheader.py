import argparse
import os
import re
import string
import sys

class HeaderConfig:
    outfile = ""
    header_guard = ""
    cxx_namespaces = []

DEFAULT_NAMESPACES = ['project']

class ParsingNamespace:
    pass

def remove_non_alphanumeric(str):
    return re.sub(r'[^A-Za-z0-9]', '', str);

def filename_to_macro_compliant_name(filepath):
    basename = os.path.basename(filepath)
    filename, file_extension = os.path.splitext(basename)
    macro = remove_non_alphanumeric(filename)
    macro += '_'
    macro += remove_non_alphanumeric(file_extension)

    return macro.upper()

def namespaces_to_header_guard(cxx_namespaces, filename):
    header_guard = "_"
    for namespace in cxx_namespaces:
        header_guard += namespace
        header_guard += "_"
    header_guard += filename_to_macro_compliant_name(filename)
    header_guard += "_"

    return header_guard.upper()

def make_parser():
    parser = argparse.ArgumentParser(
        description='Creates a baseline C++ header file with provided options',
        usage='%(prog)s [OPTIONS]')
    parser.add_argument(
        '-o',
        help='output filepath')
    parser.add_argument(
        '-n',
        nargs='*',
        default=DEFAULT_NAMESPACES,
        help='a baseline namespace for the file')
    return parser

def parse(args):
    parsed_args = ParsingNamespace()
    parser = make_parser()
    parser.parse_args(args=args, namespace=parsed_args)

    config = HeaderConfig()
    config.outfile        = parsed_args.o
    config.cxx_namespaces = parsed_args.n
    if (config.cxx_namespaces == []):
        config.cxx_namespaces = DEFAULT_NAMESPACES
    config.header_guard   = namespaces_to_header_guard(
          config.cxx_namespaces,
          parsed_args.o)

    return config

def namespaces_to_file_contents(cxx_namespace):
    open_brackets = ''
    closed_brackets = ''
    for n in cxx_namespace:
        open_brackets += 'namespace ' + n + ' {\n'
    for n in reversed(cxx_namespace):
        closed_brackets += '\n} // namespace ' + n

    return open_brackets, closed_brackets

def make_cpp_header(header_config):
    open_brackets, close_brackets = namespaces_to_file_contents(
        header_config.cxx_namespaces)
    format = string.Template(
"""#ifndef $header_guard
#define $header_guard

$open_namespaces


$close_namespaces

#endif // $header_guard

""")
    replacements = dict(
        header_guard=header_config.header_guard,
        open_namespaces=open_brackets,
        close_namespaces=close_brackets,
    )
    contents = format.safe_substitute(replacements)
    with open(header_config.outfile, 'w') as f:
        f.write(contents)

if __name__ == '__main__':
    make_cpp_header(parse(sys.argv[1:]))
    print('C++ header created')
