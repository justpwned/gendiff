from gendiff import generate_diff
import json


def test_diff():
    file1 = json.load(open('tests/fixtures/file1.json'))
    file2 = json.load(open('tests/fixtures/file2.json'))
