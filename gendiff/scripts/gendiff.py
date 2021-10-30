#!/usr/bin/env python

import argparse
import gendiff

def handle_args():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        choices=['stylish'],
        default='stylish',
        help='set format of output')
    return parser.parse_args()

def main():
    args = handle_args()

    if format == 'stylish':
        formatter = gendiff.format_stylish
    else:
        raise Exception('Unsupported output format')

    diff = gendiff.generate_diff(args.first_file, args.second_file, formatter)
    print(diff)


if __name__ == '__main__':
    main()
