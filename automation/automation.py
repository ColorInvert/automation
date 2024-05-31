from rich.console import Console
from rich.prompt import Prompt
import os

console = Console()


# Functions


# Option 1
def create_folder(name, location):

    console.print(f"name given was {name}, location given was {location}")
    pass


# Option 2
def delete_user(name):
    console.print(f"name given was {name}.")
    pass


# Option 3
def sort_by_type(location):
    console.print(f"location given was {location}")
    pass


# Option 4
def count_files(location):
    console.print(f"location given was {location}")
    filecount = len(os.listdir(location))
    console.print(f"You have {filecount} files in that directory.")


# Option 5
def parse_logs(location):
    pass


# Option 6 is just exit, so it's just the command "break"

# Direct-run Main
if __name__ == "__main__":

    # Infinite loop to keep program focus
    while True:
        console.print(
            "\n[r]Directory Helper[/r]\n\n  1.Create new [yellow]folder[/yellow]\n\n  2.[red]Delete[/red] [yellow]folder[/yellow] by moving into a temp directory\n\n  3.Sort [cyan]files[/cyan] by type\n\n  4.Parse [purple]log[/purple] [cyan]file[/cyan] for [yellow]warnings[/yellow] and [red]errors[/red]\n\n  5.Count [cyan]files[/cyan] within [yellow]folder[/yellow]\n\n  6.[purple]Exit[/purple]\n"
        )

        choice = Prompt.ask(
            "Select an option",
            choices=["1", "2", "3", "4", "5", "6"]
        )

        if choice == "1":
            name = Prompt.ask("\nEnter a [green]name[/green] for your [yellow]folder[/yellow]")
            location = Prompt.ask("\nEnter a [orange3]relative path[/orange3] destination for your [yellow]folder[/yellow]")
            create_folder(name, location)

        elif choice == "2":
            name = Prompt.ask("\nEnter the [yellow]folder[/yellow] [green]name[/green] of the user to [red]delete[/red] (files moved to temp directory)")
            delete_user(name)

        elif choice == "3":
            location = Prompt.ask("\nEnter the [orange3]relative path[/orange3] for your [green]source[/green] [yellow]folder[/yellow]")
            sort_by_type(location)
        
        elif choice == "4":
            directory = Prompt.ask("\nEnter the [orange3]relative path[/orange3] containing [purple]log[/purple] [cyan]file(s)[/cyan]")
            count_files(directory)

        elif choice == "5":
            directory = Prompt.ask("\nEnter the [orange3]relative path[/orange3] to count [cyan]files[/cyan] in")
            count_files(directory)

        # Break infinite loop to lose program focus if 6.
        else:
            break
