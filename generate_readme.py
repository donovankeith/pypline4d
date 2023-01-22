"""generate_docs.py
Creates README.md which lists all .py files in this repo.
"""

import os
import ast

def list_py_scripts(root_dir):
    header = """# pypline4d

A series of utility scripts for Maxon's Cinema 4D (c4d)"""

    toc = ""

    exclude = set(['.git'])
    
    # Need topdown to ensure predictable order for in-place remove
    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Remove "bad" directories
        dirs[:] = [d for d in dirs if d not in exclude]

        dirname = os.path.basename(root)
        print(dirname)
        if dirname.startswith("."):
            continue

        toc += f"## {dirname}\n"
        toc += "\n"
        toc += "| Name | Description |\n"
        toc += "|------|-------------|\n"

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.relpath(os.path.join(root, file), root_dir)
                with open(os.path.join(root, file), 'r') as f:
                    source = f.read()
                module = ast.parse(source)
                docstring = ast.get_docstring(module)
                if docstring:
                    lines = docstring.strip().split('\n')
                    name = None
                    description = None
                    for line in lines:
                        if line.startswith("Name-en-US:"):
                            name = line.split(':')[1].strip()
                        elif line.startswith("Description-en-US:"):
                            description = line.split(':')[1].strip()
                    if name is None:
                        name = lines[0]
                    if description is None:
                        description = lines[1]
                    toc += f"| [{name}]({filepath}) | {description} |\n"

        toc += "\n"
    with open("README.md", "w") as f:
        f.write(header)
        f.write(toc)

list_py_scripts(os.path.dirname(__file__))


def main():
    list_py_scripts(os.path.dirname(__file__))

if __name__ == "__main__":
    main()