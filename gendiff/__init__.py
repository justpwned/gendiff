import json


def stringify(value, replacer=' ', space_count=1):
    base_indent = replacer * space_count

    def walk(value, depth):
        if not isinstance(value, dict):
            return str(value)

        prev_indent = (depth - 1) * base_indent
        indent = depth * base_indent
        lines = []
        for k, v in value.items():
            value_string = walk(v, depth + 1)
            lines.append(f'{indent}{k}: {value_string}')
        result = '\n'.join(lines)
        return f'{{\n{result}\n{prev_indent}}}'

    return walk(value, 1)


def generate_diff_dict(dict1, dict2):
    pass


def generate_diff(filepath1, filepath2):
    with open(filepath1) as f1, open(filepath2) as f2:
        dict1 = json.load(f1)
        dict2 = json.load(f2)

    diff_dict = generate_diff_dict(dict1, dict2)
    return stringify(diff_dict)
