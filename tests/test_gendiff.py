from gendiff import generate_diff
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_filepath(filepath):
    return os.path.join(BASE_DIR, 'fixtures', filepath)


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def test_simple_diff():
    filepath1 = get_filepath('simple1.json')
    filepath2 = get_filepath('simple2.json')
    diffpath = get_filepath('diff_simple.json')

    assert generate_diff(filepath1, filepath2) == load_json(diffpath)


def test_nested_diff():
    filepath1 = get_filepath('nested1.json')
    filepath2 = get_filepath('nested2.json')
    diffpath = get_filepath('diff_nested.json')

    assert generate_diff(filepath1, filepath2) == load_json(diffpath)
