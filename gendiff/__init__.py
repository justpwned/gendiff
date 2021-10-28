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


def get_value_type(value):
    if isinstance(value, dict):
        return 'dict'
    elif isinstance(value, list):
        return 'list'
    return 'primitive'


# A bit hacky solution, couldn't find a way to make it more elegant without OOP
def get_value_for_type(type):
    return globals()['generate_diff_' + type]


def generate_diff_primitive(prim1, prim2):
    return {
        'old': prim1,
        'new': prim2
    }


def generate_diff_list(list1, list2):
    pass


def generate_diff_dict(old_dict, new_dict):
    """
    Diff dict semantics:

    <TYPE> := 'dict' | 'list' | 'primitive'
    <VALUE> := <DICT> | <LIST> | <PRIMITIVE>

    {
        field: {
            'state': 'added' | 'removed' | 'unchanged' | 'changed' ,
            'type': <TYPE> | { 'old': <TYPE>, 'new': <TYPE>}
            'value': <VALUE> | { 'old': <VALUE>, 'new': <VALUE> }
        }
    }
    """

    old_dict_keys = old_dict.keys()
    new_dict_keys = new_dict.keys()

    removed_keys = old_dict_keys - new_dict_keys
    added_keys = new_dict_keys - old_dict_keys
    common_keys = old_dict_keys & new_dict_keys

    diff_dict = {}

    # mark old keys as 'removed'
    for k in removed_keys:
        old_value = old_dict[k]
        diff_dict[k] = {'state': 'removed',
                        'type': get_value_type(old_value),
                        'value': old_value}

    # mark new keys as 'added'
    for k in added_keys:
        new_value = new_dict[k]
        diff_dict[k] = {'state': 'added',
                        'type': get_value_type(new_value),
                        'value': new_value}

    # update keys common to both dictionaries
    for k in common_keys:
        old_value = old_dict[k]
        old_type = get_value_type(old_value)
        new_value = new_dict[k]
        new_type = get_value_type(new_value)

        # same values => same types
        if old_value == new_value:
            diff_dict[k] = {
                'state': 'unchanged',
                'type': old_type,
                'value': old_value
            }
            continue

        # same value types
        # Note: DON'T check values for equality
        if old_type == new_type:
            diff_dict[k] = {
                'state': 'changed',
                'type': old_type,
                'value': get_value_for_type(old_type)(old_value, new_value)
            }
        else:
            diff_dict[k] = {
                'state': 'changed',
                'type': {
                    'old': old_type,
                    'new': new_type
                },
                'value': {
                    'old': old_value,
                    'new': new_value
                }
            }

    return diff_dict


def generate_diff(filepath1, filepath2):
    with open(filepath1) as f1, open(filepath2) as f2:
        dict1 = json.load(f1)
        dict2 = json.load(f2)

    return generate_diff_dict(dict1, dict2)
