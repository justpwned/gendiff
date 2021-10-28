from gendiff import generate_diff, diff_stringify
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_fixture_filepath(filepath):
    return os.path.join(BASE_DIR, 'fixtures', filepath)


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def test_simple_diff():
    filepath1 = get_fixture_filepath('simple1.json')
    filepath2 = get_fixture_filepath('simple2.json')
    diffpath = get_fixture_filepath('diff_simple.json')
    string_diffpath = get_fixture_filepath('diff_simple_string')

    diff_dict = generate_diff(filepath1, filepath2)
    assert diff_dict == load_json(diffpath)
    assert diff_stringify(diff_dict) == open(string_diffpath).read()


def test_nested_diff():
    filepath1 = get_fixture_filepath('nested1.json')
    filepath2 = get_fixture_filepath('nested2.json')
    diffpath = get_fixture_filepath('diff_nested.json')
    string_diffpath = get_fixture_filepath('diff_nested_string')

    diff_dict = generate_diff(filepath1, filepath2)
    assert diff_dict == load_json(diffpath)
    assert diff_stringify(diff_dict) == open(string_diffpath).read()
