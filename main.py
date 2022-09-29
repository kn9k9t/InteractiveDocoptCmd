from docopt import docopt, DocoptExit
from cmd import Cmd
from tabulate import tabulate
from helpers import get_cmd_completions
import readline

FILE_WITH_TASKS = "tasks.txt"

def docopt_cmd(func):
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

class CmdShell(Cmd):
    tasks = {}
    admissible_statuses = ['new', 'in-work', 'done', 'closed']
    prompt = "Tasks>"
    def __init__(self):
        Cmd.__init__(self)
        self.read_file_to_list()

    def read_file_to_list(self):
        try:
            file = open(FILE_WITH_TASKS, "r")
            for line in file.readlines():
                args = line.strip("\n").split('#')
                self.tasks[int(args[0])] = args[1:]
        except FileNotFoundError:
            pass

    def completedefault(self, text, line, begidx, endidx):
        args = []
        for line_arg in line.split():
            if line_arg == text:
                continue
            if not line_arg.startswith('-'):
                args.append(line_arg)
            else:
                break

        if not text:
            result = get_cmd_completions(self, args)
            return result

        result = get_cmd_completions(self, args)
        return [arg for arg in result if arg.startswith(text)]

    @docopt_cmd
    def do_show(self, args):
        """"Usage:
        show all
        show new
        show in-work
        show done
        show closed
        """

        for arg in args:
            if args[arg]:
                table = []
                for id, task in self.tasks.items():
                    if arg == 'all' or task[2] == arg:
                        table.append([id, task[0], task[1], task[2]])
                print(tabulate(table))
                return

    @docopt_cmd
    def do_add(self, args):
        """"Usage:
        add <name> [--description=desc] [--status=status]
        """

        if not self.tasks:
            task_id = 1
        else:
            task_id = max(self.tasks.keys()) + 1

        if not args['--description']:
            description = ''
        else:
            description = args['--description']

        if not args['--status']:
            status = 'new'
        else:
            if args['--status'] not in self.admissible_statuses:
                print('Info: Wrong status')
                return
            status = args['--status']
        self.tasks[task_id] = [args['<name>'], description, status]

        file = open(FILE_WITH_TASKS, "a")
        file.writelines(f"{task_id}#{args['<name>']}#{description}#{status}\n")
        file.close()

    @docopt_cmd
    def do_edit(self, args):
        """"Usage:
        edit name <id> <data>
        edit description <id> <data>
        edit status <id> <data>
        """

        try:
            task = self.tasks[int(args['<id>'])]
        except KeyError:
            print("Wrong task id!")
            return

        if args['name']:
            task[0] = args['<data>']

        if args['description']:
            task[1] = args['<data>']

        if args['status']:
            if args['<data>'] not in self.admissible_statuses:
                print('Info: Wrong status')
                return
            task[2] = args['<data>']

        self.tasks[int(args['<id>'])] = task

        file = open(FILE_WITH_TASKS, "w")
        for id, task in self.tasks.items():
            file.writelines(f"{id}#{task[0]}#{task[1]}#{task[2]}\n")
        file.close()

    @docopt_cmd
    def do_delete(self, args):
        """"Usage:
        delete (all|<id>)
        """

        if args['all']:
            file = open(FILE_WITH_TASKS, "w")
            self.tasks = {}
            file.close()

        else:
            try:
                self.tasks.pop(int(args['<id>']))
            except KeyError:
                print("Wrong task id!")
                return

            file = open(FILE_WITH_TASKS, "w")
            for id, task in self.tasks.items():
                file.writelines(f"{id}#{task[0]}#{task[1]}#{task[2]}\n")
            file.close()

def main():
    old_delims = readline.get_completer_delims()
    readline.set_completer_delims(old_delims.replace('-', ''))
    CmdShell().cmdloop()

if __name__ == '__main__':
    main()
