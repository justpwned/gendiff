from gendiff import generate_diff
import os


def test_diff():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath1 = os.path.join(base_dir, 'fixtures/file1.json')
    filepath2 = os.path.join(base_dir, 'fixtures/file2.json')

    with open('tests/fixtures/diff_file1_file2', 'r') as df:
        diff = df.read()

    assert generate_diff(filepath1, filepath2) == diff
