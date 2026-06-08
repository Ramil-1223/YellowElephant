from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console

console = Console()


def run_with_spinner(description: str, func, *args, **kwargs):
    with Progress(
        SpinnerColumn(),
        TextColumn(f"[bold cyan]{{task.description}}[/bold cyan]"),
        transient=True,
    ) as progress:
        progress.add_task(description=description, total=None)
        return func(*args, **kwargs)


def print_single_column_table(title: str, data: str, header_style: str = "#ff0000", data_style: str = "bold yellow"):
    table = Table()
    table.add_column(title, header_style=header_style)
    table.add_row(data, style=data_style)
    console.print(table)