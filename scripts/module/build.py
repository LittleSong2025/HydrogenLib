import subprocess as sp
import sys

import rich
import rich.traceback
from rich import print

from scripts.base import convert_to_module_name, convert_to_package_name, find_project_dir, find_module
from pathlib import Path
from scripts import uvc



def main():
    modules = sys.argv[1::]
    project_dir = find_project_dir()

    vaild_modules = []

    for module_name in modules:
        module_name = module_name.lower()
        module = find_module(module_name, project_dir)
        if module is None:
            print(f"[red]Error: module '{module_name}' not found[/red]")
            exit(1)

        print(f"Found module [bold]{module_name}[/bold]")

        vaild_modules.append((module_name, module))

    for name, module in vaild_modules:
        print(f'( {name} )\t\t[bold]Building...[/bold]')

        try:
            uvc.build(module)
            print(f"( {name} )\t\t[green]Build successful[/green]")
        except sp.CalledProcessError as e:
            print(f"( {name} )\t\t[red]Error: build failed[/red]")
            exit(1)


if __name__ == "__main__":
    main()

