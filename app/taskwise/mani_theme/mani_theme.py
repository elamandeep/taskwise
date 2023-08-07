"""
User interface used in the app
"""
# pylint: disable=C0415

import sys
from time import time
from datetime import datetime
from typing import List

import colorama
import rich
from rich.markdown import Markdown
from rich.console import Console

from taskwise.mani_theme.pretty_date import pretty_date

SELECT_MARK = "[yellow]>"
QUESTION_MARK = "[blue]?[/]"
ERROR_MARK = "[red]✕[/]"
EXCLAMATION_MARK = '[magenta]![/]'
CHECK_MARK = '[green]✓[/]'
EXIT_MARK = '[bright_black]✕[/]'

TASKS = [['c1', False, 't1', 'test task one', time()],
         ['c1', True, 't2', 'test task two', time()],
         ['c1', True, 't3', 'test task three', time()],
         ['c2', True, 't1', 'test task one', time()],
         ['c2', False, 't2', 'test task two', time()]]

CLOSE_MESSAGE = "Operation cancelled."

try:
    import msvcrt

    def getch() -> str:
        """
        Gets a single character from STDIO.
        """

        return chr(int.from_bytes(msvcrt.getch(), "little"))
except ImportError:
    import termios

    def getch():
        """
        Gets a single character from STDIO.
        """
        file_no = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_no)
        term = termios.tcgetattr(file_no)
        try:
            term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK |
                         termios.BRKINT)
            termios.tcsetattr(file_no, termios.TCSAFLUSH, term)

            character = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_no, termios.TCSADRAIN, old_settings)
        return character


IS_OS_WINDOWS = sys.platform in ("win32", "cygwin")


def getkey() -> str:
    """
    Returns the key pressed by user. if None it waits untill a key is pressed
    """
    if IS_OS_WINDOWS is False:
        character1 = getch()

        if character1 != "\x1B":
            return character1

        character2 = getch()
        if character2 not in "\x4F\x5B":
            return character1 + character2

        character3 = getch()
        if character3 not in "\x31\x32\x33\x35\x36":
            return character1 + character2 + character3

        character4 = getch()
        if character4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
            return character1 + character2 + character3 + character4

        character5 = getch()
        return character1 + character2 + character3 + character4 + character5
    else:
        character = getch()

        if character not in "\x00\xe0":
            return character

        character2 = getch()

        return "\x00" + character2


if sys.platform.startswith(("linux", "darwin", "freebsd")):
    UP = "\x1b\x5b\x41"
    DOWN = "\x1b\x5b\x42"
elif sys.platform in ("win32", "cygwin"):
    UP = "\x00\x48"
    DOWN = "\x00\x50"
DELETE = "\x12"
EXIT = "\x03"

stdout = sys.stdout


def option_selector(options: List[str], message: str) -> int:
    """
    UI option Selector

    arguments
    ---------
    options[List[str]]: options that user will have
    message[str]: message of selector
    """
    selected_option = 0

    rich.print(f'{QUESTION_MARK} {message}: [bright_black]» - Use'
               + ' arrow-keys. Return to submit.', flush=False)

    while True:
        for option_id, _option in enumerate(options):
            if option_id == selected_option:
                rich.print(f'{SELECT_MARK}   {_option}', flush=False, end='')
            else:
                rich.print(f'    {_option}', flush=False, end='')
            stdout.write("\n")
        stdout.flush()

        key = getkey()

        if key in {UP, DOWN}:
            stdout.write("\033[1A\033[2K" * len(options))
            if key == DOWN:
                if selected_option < len(options) - 1:
                    selected_option += 1
                else:
                    selected_option = 0
            elif key == UP:
                if selected_option > 0:
                    selected_option -= 1
                else:
                    selected_option = len(options) - 1
        else:
            stdout.write("\033[1A\033[2K" * (len(options)))
            stdout.flush()

            if key in '\r\n':
                stdout.write("\033[1A\033[2K")
                return selected_option
            elif key == EXIT:
                stdout.write("\033[1A\033[2K")
                rich.print(f'{ERROR_MARK} {message}:'
                           + f' [bright_black]» {options[selected_option]}.',
                           flush=False)
                rich.print(f'{EXIT_MARK} {CLOSE_MESSAGE}',
                           flush=False)
                stdout.flush()
                return


def display_tasks(tasks, category):
    """
    UI task viewer

    arguments
    ---------
    tasks[list]: a list of a tasks in this category
    category[str]: name of this category
    """
    rich.print(f'{EXCLAMATION_MARK} [bright_black]» Use arrow-keys.'
               + ' Return to toggle checkmark. Ctrl + R to delete'
               + ' selected task permanently.', flush=False)

    selected_task = 0
    tasks += [[category, None, '[blue]+', 'Add a task', None]]

    console = Console()
    additional_line_count = 0

    while True:
        for task_id, task in enumerate(tasks):
            if task[4] is None:
                date_created = ''
            else:
                date_created = pretty_date(
                    datetime.fromtimestamp(task[4])
                )
            if task not in TASKS:
                task[0] = category
                TASKS.append(task)

            if task[1] is True:
                task = f'{CHECK_MARK} {task[2]} {date_created}'
            else:
                task = f'  {task[2]} {date_created}'

            if task_id == selected_task:
                rich.print(f'{SELECT_MARK} {task}', flush=False, end='')
                print('\n' + ' ' * 8, end='', flush=False)
                with console.capture() as capture:
                    console.print(Markdown(tasks[selected_task][3]), end='')
                additional_line_count += len(capture.get().split('\n'))
                rich.print(Markdown(tasks[selected_task][3]),
                           flush=False, end='')
            else:
                rich.print(f'  {task}', flush=False, end='')
            stdout.write("\n")
        stdout.flush()

        key = getkey()

        if key in {UP, DOWN, DELETE}:
            stdout.write("\033[1A\033[2K" * (len(tasks) +
                                             additional_line_count + 1))
            additional_line_count = 0
            if key == DOWN:
                if selected_task < len(tasks) - 1:
                    selected_task += 1
                else:
                    selected_task = 0
            elif key == UP:
                if selected_task > 0:
                    selected_task -= 1
                else:
                    selected_task = len(tasks) - 1
            elif key == DELETE:
                if tasks[selected_task][1] is not None:
                    TASKS.pop(TASKS.index(tasks[selected_task]))
                    tasks.pop(selected_task)
        else:
            stdout.write("\033[1A\033[2K" * (len(tasks) +
                                             additional_line_count + 1))

            additional_line_count = 0
            stdout.flush()
            if key in '\r\n' and tasks[selected_task][1] is None:
                if tasks[selected_task][2][-1] == '+':
                    rich.print(f'{QUESTION_MARK} Choose an name'
                               + ' for this task: [bright_black]» ',
                               flush=False, end='')
                    name = input(colorama.Fore.LIGHTBLACK_EX)
                    stdout.write("\033[1A\033[2K")
                    if name.strip() != '' and (
                            name.strip() not in [task[2] for task in tasks]
                    ):
                        rich.print(f'{QUESTION_MARK} Choose an description'
                                   + ' for this task: [bright_black]» ',
                                   flush=False, end='')
                        description = input(colorama.Fore.LIGHTBLACK_EX)
                        tasks.insert(-1, [category, False, name,
                                          description, time()])
            elif key in '\r\n':
                TASKS[TASKS.index(tasks[selected_task])][1] = not (
                    TASKS[TASKS.index(tasks[selected_task])][1]
                )
                tasks[selected_task][0] = category
            elif key == EXIT:
                stdout.write("\033[1A\033[2K")
                rich.print(f'{ERROR_MARK}[bright_black] Use arrow-keys.'
                           + ' Return to toggle checkmark.', flush=False)
                rich.print(f'{EXIT_MARK} {CLOSE_MESSAGE}',
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
        display_tasks(categories[categories_names[category]],
                      categories_names[category])


option = option_selector(['Display Tasks', 'exit'], 'Select an option')
if option == 0:
    display_task_categories()
