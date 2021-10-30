import json
import yaml


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


def parse_file(filepath):
    with open(filepath) as f:
        if filepath.endswith('.yaml') or filepath.endswith('.yml'):
            return yaml.load(f.read(), Loader=yaml.SafeLoader)
        elif filepath.endswith('.json'):
            return json.loads(f.read())
        raise Exception('Unsupported data format')


def generate_diff(filepath1, filepath2, formatter):
    dict1, dict2 = parse_file(filepath1), parse_file(filepath2)
    diff_dict = generate_diff_dict(dict1, dict2)
    return formatter(diff_dict)
