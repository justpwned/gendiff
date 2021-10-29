import json


def stringify(value, replacer=' ', space_count=4, depth_start=1):
    base_indent = replacer * space_count

    def walk(value, depth):
        if not isinstance(value, dict):
            return render_primitive(value)

        prev_indent = (depth - 1) * base_indent
        indent = depth * base_indent
        lines = []
        for k, v in value.items():
            value_string = walk(v, depth + 1)
            lines.append(f'{indent}{k}: {value_string}')
        result = '\n'.join(lines)
        return f'{{\n{result}\n{prev_indent}}}'

    return walk(value, depth_start)


def render_primitive(value):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return str(value)


def render_value(value, type, **kwargs):
    if type == 'primitive':
        return render_primitive(value)
    elif type == 'dict':
        return str(stringify(value, **kwargs))


def diff_stringify(diff_dict):
    node_indents = {
        'added': '  + ',
        'removed': '  - ',
        'unchanged': '    '
    }

    def walk_default_node(key, node, depth):
        indent = node_indents[node['state']]
        node_type = node['type']
        node_value = node['value']
        # node_value contains the final value in this case, meaning that
        # we shouldn't go any deeper trying to unravel the diff tree
        # just stringify what is left of it depending on the type
        return f'{indent}{key}: {render_value(node_value, node_type, depth_start=depth + 1)}'

    def walk_changed_node(key, node, depth):
        indent = node_indents['unchanged']
        node_type = node['type']
        node_value = node['value']

        if node_type == 'primitive':
            add_indent = (depth - 1) * indent
            return f'{node_indents["removed"]}{key}: {render_value(node_value["old"], node_type)}\n'\
                   f'{add_indent}{node_indents["added"]}{key}: {render_value(node_value["new"], node_type)}'
        elif node_type == 'dict':
            dict_indent = indent
            return f'{dict_indent}{key}: {walk_diff(node_value, depth)}'
        elif node_type == 'list':
            raise Exception('List has not been implemented yet')
        else:  # type has new and old
            old_type = node_type['old']
            new_type = node_type['new']
            add_indent = (depth - 1) * indent
            old_rendered_value = render_value(
                node_value["old"], old_type, depth_start=depth + 1)
            new_rendered_value = render_value(
                node_value["new"], new_type, depth_start=depth + 1)
            return f'{node_indents["removed"]}{key}: {old_rendered_value}\n'\
                   f'{add_indent}{node_indents["added"]}{key}: {new_rendered_value}'

    def walk_node(key, node, depth):
        if node['state'] != 'changed':
            return walk_default_node(key, node, depth)

        # "changed" node returns two components
        return walk_changed_node(key, node, depth)

    def walk_diff(diff, depth):
        node_lines = []
        prev_indent = (depth - 1) * node_indents['unchanged']
        base_indent = depth * node_indents['unchanged']
        for key, node in sorted(diff.items()):
            node_string = walk_node(key, node, depth + 1)
            node_lines.append(f'{base_indent}{node_string}')
        result = '\n'.join(node_lines)
        return f'{{\n{result}\n{base_indent}}}'

    return walk_diff(diff_dict, 0)


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
