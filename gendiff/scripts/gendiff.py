#!/usr/bin/env python

import argparse
import gendiff
import json


def handle_args():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    return parser.parse_args()


def main():
    args = handle_args()
    result = gendiff.generate_diff(args.first_file, args.second_file)
    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
