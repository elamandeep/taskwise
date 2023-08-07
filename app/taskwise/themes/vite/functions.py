"""
Required functions for `models.py` and `main.py`
"""
import time
import uuid

from rich.table import Table
from rich.console import Console
from rich.progress import SpinnerColumn, Progress, TextColumn
import typer
from questionary import Choice, Style, select, autocomplete

from taskwise.models import Model, List, Task


def generate_choice():
    """
    Generates the options for the autocomplete function.
    """
    model_obj = Model()
    return [i[2] for i in model_obj.list_all_tasks()]


def generate_options(obj: Model, custom_style: List):
    """
    Generates the options for the select function.
    """
    return select(
        "Select task id",
        choices=[Choice(title=[("class:yellow", "Go Back")], value="back")]
        + list(
            Choice(title=[("class:display", str(f"{i[0]}  {i[1]}"))], value=str(i[0]))
            for i in obj.list_all_tasks()
        ),
        style=custom_style,
    ).ask()


def loader(desc: str):
    """
    Used to display a spinner
    """
    text = TextColumn("[progress.description]{task.description}")
    with Progress(SpinnerColumn(), text) as progress:
        progress.add_task(description=desc)
        time.sleep(0.5)


def display_all_tasks():
    """
    Displays all the tasks present in the database in a table
    format.
    """

    model_obj = Model()
    table = Table(
        show_header=True, header_style="Italic yellow", title="Your task list"
    )
    table.add_column("Task ID", style="yellow", width=30)
    table.add_column("Task", style="cyan", width=30)
    table.add_column("Category", style="green", width=20)
    table.add_column("Status", style="magenta", width=10)
    table.add_column("Date Added", style="red", width=20)
    table.add_column("Date Completed", style="", width=20)
    for i in model_obj.list_all_tasks():
        table.add_row(i[0], i[1], i[2], i[3], i[4], i[5])
    console = Console()
    console.print(table)

    while True:
        is_continue = typer.confirm("Do you want to go back?")
        if is_continue is True:
            loader("going back...")
            break


def insert_new_task():
    """
    This function inserts a new task into the database.
    """

    task = typer.prompt("Enter the task")
    category = autocomplete("Enter the categorys", choices=["ssss"]).ask()
    model_obj = Model()
    task_id = str(uuid.uuid4())
    task_obj = Task(task_id, task, category)
    model_obj.insert_task(task_obj)
    loader("Adding task...")
    typer.echo("Task added successfully!")


def update_task():
    """
    This function updates the task in the database.
    """
    custom_style = Style(
        [
            ("display", "fg:#083fc9 italic"),
        ]
    )
    model_obj = Model()
    task_id = generate_options(model_obj, custom_style)
    if task_id == "back":
        loader("going back...")
        return

    is_category = typer.confirm("Do you want to update the category?")
    if is_category is True:
        category = typer.prompt("Enter the category")
        model_obj.update_task(task_id, category)

    is_task = typer.confirm("Do you want to update the task?")
    if is_task is True:
        task = typer.prompt("Enter the task")
        model_obj.update_task(task_id, task)
    loader("Updating task...")
    typer.echo("Task updated successfully!")


def delete_task():
    """
    This function deletes the task from the database.
    """
    obj = Model()
    custom_style = Style(
        [
            ("display", "fg:#f44336 italic"),
        ]
    )
    task_id = generate_options(obj, custom_style)
    if task_id == "back":
        loader("going back...")
        return
    else:
        obj.delete_task(task_id)
    loader("Deleting task...")
    typer.echo("Task deleted successfully!")
