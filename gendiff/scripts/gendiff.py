#!/usr/bin/env python

import argparse
import gendiff


def handle_args():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    return parser.parse_args()


def main():
    args = handle_args()
    diff = gendiff.generate_diff(args.first_file, args.second_file)
    print(gendiff.diff_stringify(diff))


if __name__ == '__main__':
    main()
