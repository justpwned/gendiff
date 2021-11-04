import os
import pytest
from gendiff import generate_diff


def get_fixture_path(filepath):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'fixtures', filepath)


@pytest.fixture
def simple_json_paths():
    return get_fixture_path('simple1.json'),\
        get_fixture_path('simple2.json')


@pytest.fixture
def nested_json_paths():
    return get_fixture_path('nested1.json'),\
        get_fixture_path('nested2.json')


def test_simple_diff_json_format(simple_json_paths):
    with open(get_fixture_path('diff_simple.json')) as f:
        diff = f.read()

    assert generate_diff(*simple_json_paths, 'json') == diff


def test_nested_diff_json_format(nested_json_paths):
    with open(get_fixture_path('diff_nested.json')) as f:
        diff = f.read()

    assert generate_diff(*nested_json_paths, 'json') == diff


def test_simple_diff_stylish_format(simple_json_paths):
    with open(get_fixture_path('diff_simple_stylish')) as f:
        diff = f.read()

    assert generate_diff(*simple_json_paths, 'stylish') == diff


def test_nested_diff_stylish_format(nested_json_paths):
    with open(get_fixture_path('diff_nested_stylish')) as f:
        diff = f.read()

    assert generate_diff(*nested_json_paths, 'stylish') == diff


def test_simple_diff_plain_format(simple_json_paths):
    with open(get_fixture_path('diff_simple_plain')) as f:
        diff = f.read()

    assert generate_diff(*simple_json_paths, 'plain') == diff


def test_nested_diff_plain_format(nested_json_paths):
    with open(get_fixture_path('diff_nested_plain')) as f:
        diff = f.read()

    assert generate_diff(*nested_json_paths, 'plain') == diff
