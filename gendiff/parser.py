import json
import yaml


def parse_file(filepath):
    with open(filepath) as f:
        if filepath.endswith('.yaml') or filepath.endswith('.yml'):
            return yaml.load(f.read(), Loader=yaml.SafeLoader)
        elif filepath.endswith('.json'):
            return json.loads(f.read())
        raise Exception('Unsupported data format')
