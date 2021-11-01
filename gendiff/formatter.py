import json


def stringify_dict(value, replacer=' ', space_count=4, **kwargs):
    base_indent = replacer * space_count
    depth_start = kwargs.get('depth_start', 1)

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


def render_primitive(value, str_wrapper=''):
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        return f'{str_wrapper}{value}{str_wrapper}'
    return str(value)


def render_value(value, type, *, render_complex=True, str_wrapper='', **kwargs):
    if type == 'primitive':
        return render_primitive(value, str_wrapper)

    if not render_complex:
        return '[complex value]'

    if type == 'dict':
        return str(stringify_dict(value, **kwargs))

    raise Exception(f'Type {type} is not supported for rendering')


def format_stylish(diff_dict):  # noqa: C901
    node_indents = {
        'added': '  + ',
        'removed': '  - ',
        'unchanged': '    '
    }

    # default node - any node except "updated"
    def walk_default_node(key, node, depth):
        indent = node_indents[node['state']]
        # node_value contains the final value in this case, meaning that
        # we shouldn't go any deeper trying to unravel the diff tree
        # just stringify what is left of it depending on the type
        rendered_value = render_value(
            node['value'], node['type'], depth_start=depth + 1)
        return f'{indent}{key}: {rendered_value}'

    def walk_updated_node(key, node, depth):
        indent = node_indents['unchanged']
        node_type = node['type']
        node_value = node['value']

        if node_type == 'primitive':
            add_indent = (depth - 1) * indent
            old_value = render_value(node_value["old"], node_type)
            new_value = render_value(node_value["new"], node_type)
            return f'{node_indents["removed"]}{key}: {old_value}\n'\
                   f'{add_indent}{node_indents["added"]}{key}: {new_value}'
        elif node_type == 'dict':
            dict_indent = indent
            return f'{dict_indent}{key}: {walk_diff(node_value, depth)}'
        elif node_type == 'list':
            raise Exception('List has not been implemented yet')
        else:  # type has new and old
            old_type = node_type['old']
            new_type = node_type['new']
            add_indent = (depth - 1) * indent
            old_value = render_value(
                node_value["old"], old_type, depth_start=depth + 1)
            new_value = render_value(
                node_value["new"], new_type, depth_start=depth + 1)
            return f'{node_indents["removed"]}{key}: {old_value}\n'\
                   f'{add_indent}{node_indents["added"]}{key}: {new_value}'

    def walk_node(key, node, depth):
        if node['state'] == 'updated':
            return walk_updated_node(key, node, depth)
        return walk_default_node(key, node, depth)

    def walk_diff(diff, depth):
        node_lines = []
        base_indent = depth * node_indents['unchanged']
        for key, node in sorted(diff.items()):
            node_string = walk_node(key, node, depth + 1)
            node_lines.append(f'{base_indent}{node_string}')
        result = '\n'.join(node_lines)
        return f'{{\n{result}\n{base_indent}}}'

    return walk_diff(diff_dict, 0)


def format_plain(diff_dict):  # noqa: C901
    def render_value_plain(*args, **kwargs):
        return render_value(
            *args, **kwargs,
            render_complex=False,
            str_wrapper='\'')

    def fullname(names):
        return ".".join(names)

    def walk_updated_node(node, names):
        node_type = node['type']
        node_value = node['value']
        if node_type == 'primitive':
            old_value = render_value_plain(node_value['old'], node_type)
            new_value = render_value_plain(node_value['new'], node_type)
            return f'Property \'{fullname(names)}\' was updated. '\
                   f'From {old_value} to {new_value}'
        elif node_type == 'dict':
            return walk(node_value, names)
        elif node_type == 'list':
            raise Exception('List has not been implemented yet')
        else:
            old_type = node_type['old']
            new_type = node_type['new']
            old_value = render_value_plain(node_value['old'], old_type)
            new_value = render_value_plain(node_value['new'], new_type)
            return f'Property \'{fullname(names)}\' was updated. '\
                   f'From {old_value} to {new_value}'

    def walk_default_node(node, names):
        state = node['state']
        line = f'Property \'{fullname(names)}\' was {state}'
        if state == 'added':
            result = render_value_plain(node['value'], node['type'])
            line = f'{line} with value: {result}'
        return line

    def walk(diff, names):
        lines = []
        for key in sorted(diff.keys()):
            new_names = names + [key]
            node = diff[key]
            state = node['state']
            if state == 'unchanged':
                continue

            if state == 'updated':
                line = walk_updated_node(node, new_names)
            else:
                line = walk_default_node(node, new_names)

            lines.append(line)
        return '\n'.join(lines)

    return walk(diff_dict, [])


def format_json(diff_dict):
    return json.dumps(diff_dict, indent=4, sort_keys=True).strip()
