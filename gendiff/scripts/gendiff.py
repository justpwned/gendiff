#!/usr/bin/env python

import argparse
import gendiff


def handle_args():
    parser = argparse.ArgumentParser(
        description='Compare two documents. Supported formats: JSON, YAML')
    parser.add_argument('first_file', help='Old file')
    parser.add_argument('second_file', help='New file')
    parser.add_argument(
        '-f', '--format',
        choices=['stylish', 'plain', 'json'],
        default='stylish',
        help='Set format of output (default: stylish)')
    return parser.parse_args()


def main():
    args = handle_args()
    diff = gendiff.generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == '__main__':
    main()
