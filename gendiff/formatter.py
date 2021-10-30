__all__ = ['format_stylish']

def stringify_dict(value, replacer=' ', space_count=4, depth_start=1):
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
        return str(stringify_dict(value, **kwargs))


def format_stylish(diff_dict):
    node_indents = {
        'added': '  + ',
        'removed': '  - ',
        'unchanged': '    '
    }

    def walk_default_node(key, node, depth):
        indent = node_indents[node['state']]
        # node_value contains the final value in this case, meaning that
        # we shouldn't go any deeper trying to unravel the diff tree
        # just stringify what is left of it depending on the type
        rendered_value = render_value(
            node['value'], node['type'], depth_start=depth + 1)
        return f'{indent}{key}: {rendered_value}'

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