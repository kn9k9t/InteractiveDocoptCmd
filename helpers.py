def get_striped_cmd(line):
    args = line.split()
    cmd = ''
    for arg in args:
        if arg.startswith('[-'):
            arg = arg.replace('[', '')
            arg = arg.replace(']', '')
            if '=' in arg:
                arg = arg.partition('=')[0]
            else:
                arg = arg.partition(' ')[0]

        elif arg.startswith('[<'):
            continue
        cmd += arg + ' '
    return cmd


def get_cmds_list_from_doc(doc):
    cmds_list = []
    cmd = ''
    for arg in doc.split("\n")[1:]:
        arg = arg[8:]
        if arg.startswith(' '):
            cmd += get_striped_cmd(arg)

        else:
            if cmd:
                cmds_list.append(cmd.strip())
            cmd = get_striped_cmd(arg)

    return cmds_list


def get_cmds_tree_from_doc(doc):
    cmds_list = get_cmds_list_from_doc(doc)
    cmds_tree = {}
    for cmd in cmds_list:
        link_to_cmds_tree = cmds_tree
        cmd_args = cmd.split()
        for arg in cmd_args:
            if arg.startswith('-'):
                link_to_cmds_tree[arg] = {}
                continue

            if arg not in link_to_cmds_tree.keys():
                link_to_cmds_tree[arg] = {}
                link_to_cmds_tree = link_to_cmds_tree[arg]

            else:
                link_to_cmds_tree = link_to_cmds_tree[arg]

    return cmds_tree.copy()


def get_cmd_completions(obj, list_args):
    doc = getattr(obj, f"do_{list_args[0]}").__doc__
    args_tree = get_cmds_tree_from_doc(doc)
    result = []
    for arg in list_args:
        if arg in args_tree:
            args_tree = args_tree[arg]
            result = list(args_tree.keys())
        else:
            return []
    return result