import gendiff.formatter as formatter
import gendiff.parser as parser


def get_type(value):
    if isinstance(value, dict):
        return 'dict'
    elif isinstance(value, list):
        return 'list'
    return 'primitive'


def get_gendiff_func(type):
    type_to_func = {
        'primitive': generate_diff_primitive,
        'list': generate_diff_list,
        'dict': generate_diff_dict
    }
    func = type_to_func.get(type)
    if func is not None:
        return func

    raise Exception('Unsupported type')


def generate_diff_primitive(prim1, prim2):
    return {
        'old': prim1,
        'new': prim2
    }


def generate_diff_list(list1, list2):
    pass


def create_diff_node(state, type, value,
                     *, updated_type=False, updated_value=False):
    if updated_type:
        type = {
            'old': type[0],
            'new': type[1]
        }

    if updated_value:
        value = {
            'old': value[0],
            'new': value[1]
        }

    return {
        'state': state,
        'type': type,
        'value': value
    }


def generate_diff_dict(old_dict, new_dict):
    old_dict_keys = old_dict.keys()
    new_dict_keys = new_dict.keys()

    removed_keys = old_dict_keys - new_dict_keys
    added_keys = new_dict_keys - old_dict_keys
    common_keys = old_dict_keys & new_dict_keys

    removed_dict = {k: create_diff_node(
        'removed', get_type(old_dict[k]), old_dict[k]) for k in removed_keys}
    added_dict = {k: create_diff_node(
        'added', get_type(new_dict[k]), new_dict[k]) for k in added_keys}

    updated_dict = {}
    # update keys common to both dictionaries
    for k in common_keys:
        old_value = old_dict[k]
        old_type = get_type(old_value)
        new_value = new_dict[k]
        new_type = get_type(new_value)

        # same values => same types
        if old_value == new_value:
            updated_dict[k] = create_diff_node('unchanged', old_type, old_value)
            continue

        # same value types
        # Note: DON'T check values for equality
        if old_type == new_type:
            updated_dict[k] = create_diff_node(
                'updated', old_type, get_gendiff_func(old_type)(old_value, new_value))
        else:
            updated_dict[k] = create_diff_node(
                'updated',
                (old_type, new_type),
                (old_value, new_value),
                updated_type=True,
                updated_value=True)

    return {**removed_dict, **added_dict, **updated_dict}


def generate_diff(filepath1, filepath2, format_name):
    dict1, dict2 = parser.parse_file(filepath1), parser.parse_file(filepath2)
    diff_dict = generate_diff_dict(dict1, dict2)

    if format_name == 'stylish':
        return formatter.format_stylish(diff_dict)
    elif format_name == 'plain':
        return formatter.format_plain(diff_dict)
    elif format_name == 'json':
        return formatter.format_json(diff_dict)
    else:
        raise Exception('Unsupported output format')
