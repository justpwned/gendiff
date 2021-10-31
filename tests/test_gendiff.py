import os
from gendiff import generate_diff

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_fixture_filepath(filepath):
    return os.path.join(BASE_DIR, 'fixtures', filepath)


# TODO: Move file loading into separate fixtures for simple and nested tests

def test_simple_diff_json_format():
    json1 = get_fixture_filepath('simple1.json')
    json2 = get_fixture_filepath('simple2.json')
    with open(get_fixture_filepath('diff_simple.json')) as f:
        diff = f.read()

    assert generate_diff(json1, json2, 'json') == diff


def test_nested_diff_json_format():
    json1 = get_fixture_filepath('nested1.json')
    json2 = get_fixture_filepath('nested2.json')
    with open(get_fixture_filepath('diff_nested.json')) as f:
        diff = f.read()

    assert generate_diff(json1, json2, 'json') == diff


def test_simple_diff_stylish_format():
    json1 = get_fixture_filepath('simple1.json')
    json2 = get_fixture_filepath('simple2.json')
    with open(get_fixture_filepath('diff_simple_stylish')) as f:
        diff = f.read()

    assert generate_diff(json1, json2, 'stylish') == diff


def test_nested_diff_stylish_format():
    json1 = get_fixture_filepath('nested1.json')
    json2 = get_fixture_filepath('nested2.json')
    with open(get_fixture_filepath('diff_nested_stylish')) as f:
        diff = f.read()

    assert generate_diff(json1, json2, 'stylish') == diff


def test_simple_diff_plain_format():
    json1 = get_fixture_filepath('simple1.json')
    json2 = get_fixture_filepath('simple2.json')
    with open(get_fixture_filepath('diff_simple_plain')) as f:
        diff = f.read()

    assert generate_diff(json1, json2, 'plain') == diff


def test_nested_diff_plain_format():
    json1 = get_fixture_filepath('nested1.json')
    json2 = get_fixture_filepath('nested2.json')
    with open(get_fixture_filepath('diff_nested_plain')) as f:
        diff = f.read()

    assert generate_diff(json1, json2, 'plain') == diff
