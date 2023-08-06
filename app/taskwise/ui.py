"""
User interface used in the app
"""
# pylint: disable=C0415

import sys
from typing import List

import rich.console
import rich

TASKS = [['c1', False, 't1'], ['c1', True, 't2'], ['c1', True, 't3'],
         ['c2', True, 't1'], ['c2', False, 't2']]
CLOSE_MESSAGE = "Operation cancelled."
RICH_COSOLE = rich.console.Console()


try:
    import msvcrt

    def getch() -> str:
        """
        Gets a single character from STDIO.
        """

        return chr(int.from_bytes(msvcrt.getch(), "little"))
except ImportError:
    def getch():
        """
        Gets a single character from STDIO.
        """
        import tty
        import termios
        file_number = sys.stdin.fileno()
        old = termios.tcgetattr(file_number)
        try:
            tty.setraw(file_number)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_number, termios.TCSADRAIN, old)

if sys.platform.startswith(("linux", "darwin", "freebsd")):
    UP = "\x1b\x5b\x41"
    DOWN = "\x1b\x5b\x42"
elif sys.platform in ("win32", "cygwin"):
    UP = "\xe0\x48"
    DOWN = "\xe0\x50"

stdout = sys.stdout


def option_selector(options: List[str], message: str) -> int:
    """
    UI Option Selector

    arguments
    ---------
    options[List[str]]: options that user will have
    message[str]: message of selector
    """
    selected_option = 0

    rich.print(f'[blue]?[/] {message}: [bright_black]» - Use arrow-keys.'
               + ' Return to submit.', flush=False)

    while True:
        for option_id, _option in enumerate(options):
            if option_id == selected_option:
                rich.print(f'>   [u]{_option}', flush=False, end='')
            else:
                rich.print(f'    {_option}', flush=False, end='')
            stdout.write("\n")
        stdout.flush()

        if sys.platform.startswith(("linux", "darwin", "freebsd")):
            character = getch()
            if character[-1] in "\x4F\x5B":
                character += getch()
            if character[-1] in "\x31\x32\x33\x35\x36":
                character += getch()
        elif sys.platform in ("win32", "cygwin"):
            character = getch()
            if character in '\x00\xe0':
                character += getch()

        if character in {UP, DOWN}:
            stdout.write("\033[1A\033[2K" * len(options))
            if character == DOWN:
                if selected_option < len(options) - 1:
                    selected_option += 1
                else:
                    selected_option = 0
            elif character == UP:
                if selected_option > 0:
                    selected_option -= 1
                else:
                    selected_option = len(options) - 1
        else:
            stdout.write("\033[1A\033[2K" * (len(options) + 1))
            stdout.flush()

            if character in '\r\n':
                return selected_option
            else:
                rich.print(f'[red]❌[/] {message}:'
                           + f' [bright_black]» {options[selected_option]}.',
                           flush=False)
                rich.print(f'[bright_black]❌[/] {CLOSE_MESSAGE}',
                           flush=False)
                stdout.flush()
                return


def display_tasks(tasks, category):
    """
    Returns based on given filters
    """
    rich.print('[magenta]![/] [bright_black]» Use arrow-keys.'
               + ' Return to toggle checkmark.', flush=False)

    selected_task = 0
    tasks += [[category, None, '[blue]+']]

    while True:
        for task_id, task in enumerate(tasks):
            if task[1] is True:
                task = f'✔️ {task[2]}'
            else:
                task = f'  {task[2]}'
            if task_id == selected_task:
                rich.print(f'> [u]{task}', flush=False, end='')
            else:
                rich.print(f'  {task}', flush=False, end='')
            stdout.write("\n")
        stdout.flush()

        if sys.platform.startswith(("linux", "darwin", "freebsd")):
            character = getch()
            if character[-1] in "\x4F\x5B":
                character += getch()
            if character[-1] in "\x31\x32\x33\x35\x36":
                character += getch()
        elif sys.platform in ("win32", "cygwin"):
            character = getch()
            if character in '\x00\xe0':
                character += getch()

        if character in {UP, DOWN}:
            stdout.write("\033[1A\033[2K" * len(tasks))
            if character == DOWN:
                if selected_task < len(tasks) - 1:
                    selected_task += 1
                else:
                    selected_task = 0
            elif character == UP:
                if selected_task > 0:
                    selected_task -= 1
                else:
                    selected_task = len(tasks) - 1
        else:
            stdout.write("\033[1A\033[2K" * len(tasks))
            stdout.flush()
            if character in '\r\n' and tasks[selected_task][1] is None:
                if tasks[selected_task][2][-1] == '+':
                    name = RICH_COSOLE.input('[blue]?[/] Choose an name for'
                                             + ' this task: [bright_black]» ')
                    stdout.write("\033[1A\033[2K")
                    TASKS.insert(0, [category, False, name])
            elif character in '\r\n':
                TASKS[TASKS.index(tasks[selected_task])][1] = not (
                    TASKS[TASKS.index(tasks[selected_task])][1]
                )
            else:
                stdout.write("\033[1A\033[2K")
                rich.print('[red]❌[/][bright_black] Use arrow-keys.'
                           + ' Return to toggle checkmark.', flush=False)
                rich.print(f'[bright_black]❌[/] {CLOSE_MESSAGE}',
                           flush=False)
                stdout.flush()
                return


def display_task_categories():
    """
    Displays task categories
    """
    categories = {}
    for task in TASKS:
        if task[0] not in categories:
            categories.update({task[0]: [task]})
        else:
            categories[task[0]].append(task)

    categories_names = list(categories.keys())
    category = option_selector(categories_names, 'Select a category')
    if category is not None:
        display_tasks(categories[categories_names[category]], category)


option = option_selector(['Display Tasks', 'exit'], 'Select an option')
if option == 0:
    display_task_categories()
