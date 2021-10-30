import os
from gendiff import generate_diff, format_stylish

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_fixture_filepath(filepath):
    return os.path.join(BASE_DIR, 'fixtures', filepath)


def test_simple_diff_stylish():
    json1 = get_fixture_filepath('simple1.json')
    json2 = get_fixture_filepath('simple2.json')
    yaml1 = get_fixture_filepath('simple1.yaml')
    yaml2 = get_fixture_filepath('simple2.yaml')
    with open(get_fixture_filepath('diff_simple_string')) as f:
        simple_diff = f.read()
        
    assert generate_diff(json1, json2, format_stylish) == simple_diff
    assert generate_diff(yaml1, yaml2, format_stylish) == simple_diff


def test_nested_diff_stylish():
    json1 = get_fixture_filepath('nested1.json')
    json2 = get_fixture_filepath('nested2.json')
    yaml1 = get_fixture_filepath('nested1.yaml')
    yaml2 = get_fixture_filepath('nested2.yaml')
    with open(get_fixture_filepath('diff_nested_string')) as f:
        nested_diff = f.read()

    assert generate_diff(json1, json2, format_stylish) == nested_diff
    assert generate_diff(yaml1, yaml2, format_stylish) == nested_diff
