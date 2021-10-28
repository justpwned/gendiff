import json
import copy


# def diff_stringify(diff):
#     sorted_keys = sorted(diff.keys())
#     for k, v in sorted(diff.items()):
#         if v['state']


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
        return 'object'
    elif isinstance(value, list):
        return 'array'
    return 'primitive'


def generate_diff_list(list1, list2):
    pass


def generate_diff_dict(old_dict, new_dict):
    """
    Diff dict structure
    {
        field: {
            'state': 'added' | 'removed' | 'unchanged' | 'changed' ,
            'type': 'object' | 'array' | 'primitive'
            'value': value | { 'old': old_value, 'new': new_value }
            'children': [...] | {...} | None
        }
    }
    First implement only dict support!
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

        # same types, same values
        if old_value == new_value:
            diff_dict[k] = {'state': 'unchanged',
                            'type': old_type,
                            'value': old_value}
            continue

        # if old_type == new_type:
        #     if old_type == 'primitive':
        #         pass
        #     elif old_type == 'array':
        #         pass
        #     elif old_type == 'dict':
        #         pass
        #     else:
        # else:


        # different types, different values
        if old_type != new_type:
            diff_dict[k] = {'state': 'changed',
                            'type': {
                                'old': old_type,
                                'new': new_type
                            },
                            'value': {
                                'old': old_value,
                                'new': new_value
                            }}
        else:  # same types, different values
            if old_type != 'primitive':
                diff_dict[k] = {'state': 'changed',
                                'type': old_type,
                                'value': generate_diff_dict(old_value, new_value)}
            else:
                diff_dict[k] = {'state': 'changed',
                                'type': old_type,
                                'value': {
                                    'old': old_value,
                                    'new': new_value
                                }}

    return diff_dict


def generate_diff(filepath1, filepath2):
    with open(filepath1) as f1, open(filepath2) as f2:
        dict1 = json.load(f1)
        dict2 = json.load(f2)

    return generate_diff_dict(dict1, dict2)
