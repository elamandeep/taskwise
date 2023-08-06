"""
Taskwise
"""
import time
import sys

import typer
import rich
from rich.progress import track
from questionary import Choice, Style, select

from taskwise.functions import (
    display_all_tasks,
    update_task,
    insert_new_task,
    delete_task,
    loader
)


def greet():
    """
    Greets users
    """
    time.sleep(0.1)
    rich.print("[red]Welcome to TaskWise!")

    for _ in track(range(2), description="Loading..."):
        time.sleep(0.1)


def clear_terminal():
    """
    Clears the terminal
    """
    print("\x1b[2J\x1b[H")


def menu():
    """
    Displays menu
    """
    clear_terminal()

    custom_style = Style([
        ("display", "fg:#f44336 bold"),
        ("insert", "fg:#673ab7 bold"),
        ("update", "fg:#cc5454 bold"),
        ("delete", "fg:#f5b705 italic"),
        ("exit", "fg:#6bf716 italic"),
    ])
    choices = [
                    Choice(title=[("class:display", "Display all Tasks")],
                           value="display"),
                    Choice(title=[("class:insert", "Insert New Task")],
                           value="insert"),
                    Choice(title=[("class:update", "Update Task")],
                           value="update"),
                    Choice(title=[("class:delete", "Delete Task")],
                           value="delete"),
                    Choice(title=[("class:exit", "Exit")],
                           value="exit"),
               ]
    answer = select(
        "What do you want to do?",
        choices=choices,
        style=custom_style
    ).ask()

    match answer:
        case "display":
            display_all_tasks()
        case "insert":
            insert_new_task()
        case "update":
            update_task()
        case "delete":
            delete_task()
        case "exit":
            loader("Exiting...")
            sys.exit()


def main():
    """
    Main function
    """
    greet()
    while True:
        menu()
        time.sleep(0.5)


if __name__ == "__main__":
    typer.run(main)
