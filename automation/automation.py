from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import re
import os
import shutil

console = Console()

# Subfunctions:


# ?Scans a directory for a file that matches the filename regex, opens it,
# ?returns list of regex matches within that file.
def file_regex_find(regex, location, filename_regex):

    matches = []

    try:
        # This will fail if invalid source directory
        directory_list = os.listdir(location)

        # Iterate through directory list
        for filename in directory_list:

            # Check for a filename_regex input match.
            if re.search(filename_regex, str(filename)):

                file_path = os.path.join(location, filename)

                # Open file, save contents as string, regex scan for matches.
                with open(file_path, "r") as file:
                    file_contents = file.read()
                    console.print(f"File contents for {file_path}:\n{file_contents}")
                    # Return list of regex matches in string.
                    found_matches = re.findall(regex, file_contents, re.MULTILINE)
                    matches.extend(found_matches)

        # Did we find any matches in any of the files we found?
        if matches:
            return matches

        else:
            console.print("[red]No regex matches found in directory.[/red]")
            return False

    except FileNotFoundError:
        console.print("[red]Source directory not found.[/red]")
        return False

    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
        return False


# ?Creates a directory if it doesn't exist, but does not throw error if it does.
def quick_directory(name, location):
    try:
        os.listdir(location)

    except FileNotFoundError:
        console.print("[red]Directory not found.[/red]")
        return

    try:
        path = os.path.join(location, name)
        os.mkdir(path)
        return
    except:
        return


# ? Checks if file or folder exists in directory, and moves file to target.
# ? Will return True or False depending if a file was found and transferred.
def find_move(name, location, target):
    try:
        # This will fail if invalid source directory
        directory_list = os.listdir(location)

        # Iterate through directory list, to look for something called {name}
        for i in range(len(directory_list)):

            # Check for a literal name match
            if directory_list[i] == name:

                # Get paths of origin file/folder, and destination folder
                origin = os.path.join(location, str(directory_list[i]))
                destination = os.path.join(location, target)

                # Move origin file/folder into destination folder.
                shutil.move(origin, destination)
                return True
        console.print("[red]File/folder with specified name not found.[/red]")
        return False

    except FileNotFoundError:
        console.print("[red]Source directory not found.[/red]")
        return False


# ? The same as find_move above, but takes regex input instead of looking
# ? for a name match.
def find_move_regex(regex, location, target):
    try:
        # This will fail if invalid source directory
        directory_list = os.listdir(location)

        # Iterate through directory list
        for i in range(len(directory_list)):

            # Check for a regex input match.
            if re.search(regex, directory_list[i]) is not None:

                # Get paths of origin file/folder, and destination folder
                origin = os.path.join(location, str(directory_list[i]))
                destination = os.path.join(location, target)

                # Move origin file/folder into destination folder.
                shutil.move(origin, destination)
                return True
        console.print("[red]No regex matches found in directory.[/red]")
        return False

    except FileNotFoundError:
        console.print("[red]Source directory not found.[/red]")
        return False


# Functions


#! FUNCTIONAL, DON'T TOUCH
# Option 1, create new folder
def create_folder(name, location):

    console.print(f"name given was {name}, location given was {location}")
    # Check if input location exists, and exit function if not
    try:
        os.listdir(location)

    except FileNotFoundError:
        console.print("[red]Directory not found.[/red]")
        return

    try:
        path = os.path.join(location, name)

        os.mkdir(path)
    except OSError as error:
        console.print(f"[red]{error}[/red]")


#! FUNCTIONAL, DON'T TOUCH
# Option 2 Delete user folder (does not actually delete, but moves to temp)
def delete_user(name, location):

    # Prevent user from trying to move something already called temp to a temp folder
    if name == "temp":
        console.print(
            f"[red]Please name your directory literally anything but 'temp'.[/red]"
        )
        return

    # make "temp" directory if not present
    quick_directory("temp", location)
    # Move named file or folder to temp.

    if find_move(name, location, "temp") == True:
        console.print(
            f"[green] file or folder successfully moved into temp folder for archived deletion.[/green]"
        )


#! FUNCTIONAL, DON'T TOUCH
# Option 3 Sort files by type
def sort_by_type(location):

    # If log and mail directories dont exist, make them.
    quick_directory("logs", location)
    quick_directory("mail", location)

    # Search all files in directory for .log or .mail, and move them into
    # their respective folders.
    find_move_regex(r"(.log)", location, "logs")
    find_move_regex(r"(.mail)", location, "mail")
    console.print(
        f"[green] Any existing .log or .mail files have been transferred into their respective folders.[/green]"
    )


# Option 4 Iterate through log files for warnings and errors
def parse_logs(location):

    # Define empty log entries list
    log_entries = []

    # Regex definitions for log file parsing
    logfile_regex = r"\.log"
    warning_regex = r"^.*WARNING:.*$"
    error_regex = r"^.*ERROR:.*$"

    # Collect warning log entries
    log_entries.extend(file_regex_find(warning_regex, location, logfile_regex))
    console.print(f"Our warning log list looks like {log_entries}")

    string = f"\n".join(log_entries)
    console.print(f"string looks like {string}")

    # Write to warnings.log file in current directory.
    with open("warnings.log", "w") as file:
        file.write(string)

    # Move file to location of log file.
    find_move("warnings.log", ".", location)

    # Collect error log entries
    log_entries = file_regex_find(error_regex, location, logfile_regex)
    console.print(f"Our error log list now looks like {log_entries}")

    string = f"\n".join(log_entries)
    console.print(f"string looks like {string}")

    # Write to errors.log file in current directory.
    with open("errors.log", "w") as file:
        file.write(string)

    # Move file to location of log file.
    find_move("errors.log", ".", location)


#! FUNCTIONAL, DON'T TOUCH
# Option 5 Count number of files with extension in directory
def count_files(extension, location):
    console.print(f"location given was {location}")
    # Convert string input into regex
    regex = re.compile(extension)

    # Make matches list
    matches = []

    try:
        # This will fail if invalid source directory
        directory_list = os.listdir(location)

        # Iterate through directory list
        for i in range(len(directory_list)):

            # Check for a regex input match.
            if re.search(regex, directory_list[i]) is not None:
                matches.append(directory_list[i])

        console.print(
            f"\nThere are {len(matches)} files of {extension} type in this directory."
        )
    except FileNotFoundError:
        console.print("[red]Directory not found.[/red]")


# Option 6 is just exit, so it's just the command "break"


# Direct-run Main
if __name__ == "__main__":

    # Infinite loop to keep program focus
    while True:
        console.print(
            "\n[r]Directory Helper[/r]\n\n  1.Create new [yellow]folder[/yellow]\n\n  2.[red]Delete[/red] [yellow]folder[/yellow] by moving into a temp directory\n\n  3.Sort [cyan]files[/cyan] by type\n\n  4.Parse [purple]log[/purple] [cyan]file[/cyan] for [yellow]warnings[/yellow] and [red]errors[/red]\n\n  5.Count [cyan]files[/cyan] within [yellow]folder[/yellow]\n\n  6.[purple]Exit[/purple]\n"
        )

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"])

        #! FUNCTIONAL, DON'T TOUCH
        # Option 1, create new folder
        if choice == "1":
            name = Prompt.ask(
                "\nEnter a [green]name[/green] for your [yellow]folder[/yellow]"
            )
            location = Prompt.ask(
                "\nEnter a [orange3]relative path[/orange3] destination for your [yellow]folder[/yellow]"
            )
            create_folder(name, location)

        #! FUNCTIONAL, DON'T TOUCH
        # Option 2 Delete user folder (does not actually delete, but moves to temp)
        elif choice == "2":

            location = Prompt.ask(
                "\nEnter the [orange3]relative path[/orange3] that contains your [green]source[/green] [yellow]folder[/yellow]"
            )

            name = Prompt.ask(
                "\nEnter the [cyan]name[/cyan] of the [cyan]file[/cyan] or [yellow]folder[/yellow] to [red]delete[/red] (files moved to temp directory)"
            )
            delete_user(name, location)

        #! FUNCTIONAL, DON'T TOUCH
        # Option 3 Sort files by type
        elif choice == "3":
            location = Prompt.ask(
                "\nEnter the [orange3]relative path[/orange3] for your [green]source[/green] [yellow]folder[/yellow] containing [purple]log[/purple] or mail [cyan]file(s)[/cyan]"
            )
            sort_by_type(location)

        # Option 4 Iterate through log files for warnings and errors
        elif choice == "4":
            directory = Prompt.ask(
                "\nEnter the [orange3]relative path[/orange3] containing [purple]log[/purple] [cyan]file(s)[/cyan]"
            )
            parse_logs(directory)

        #! FUNCTIONAL, DON'T TOUCH
        # Option 5 Count number of files in directory
        elif choice == "5":
            extension = Prompt.ask(
                "\nEnter the file extension of the [cyan]file[/cyan] type to count"
            )
            directory = Prompt.ask(
                "\nEnter the [orange3]relative path[/orange3] to count [cyan]files[/cyan] in"
            )
            count_files(extension, directory)

        # Break infinite loop to lose program focus if 6.
        else:
            break
