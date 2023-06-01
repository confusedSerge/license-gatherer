"""
This file reads in a yarn.lock file and uses the node_modules directory and generates a license file of the form:

--------------------------------
Package: <package name>
Version: <package version>
License: <package license>
License Text:

<package license text>

--------------------------------

The license file is written to the current directory.
"""

import argparse
import os
import re
import sys

from collections import defaultdict
from typing import Dict, List, Tuple


def split_lockfile(lockfile: str) -> List[str]:
    """
    Splits a yarn.lock file into a list of packages.
    """
    return lockfile.split("\n\n")


def parse_package(package: str) -> Tuple[str, str]:
    """
    Parses a package into a tuple of (name, version).
    """
    split_package = package.split("\n")
    index = 1 if split_package[0] == "" else 0

    name = split_package[index]
    cleaned_name = name.replace('"', "")
    
    # check if the package is prefixed with @
    if cleaned_name.startswith("@"):
        name = "@" + cleaned_name.split("@")[1]
    else:
        name = cleaned_name.split("@")[0]

    # find the version in the package
    version = split_package[index + 1]
    version = version.strip()
    version = version.removeprefix("version ")
    version = version.replace('"', "")

    return (name, version)


def load_license_text(package_name: str, node_modules_dir: str) -> str:
    """
    Loads the license text for a package.
    If the license text is not found, returns an empty string.
    """
    package_dir = os.path.join(node_modules_dir, package_name)

    # find the license file
    license_file = os.path.join(package_dir, "LICENSE")
    if not os.path.isfile(license_file):
        return ""

    # read in the license file
    with open(license_file, "r") as f:
        license_text = f.read()

    return license_text




def generate_license_text(package: str, node_modules_dir: str) -> str:
    """
    Generates a license file for a package.
    """
    name, version = parse_package(package)
    license_text = load_license_text(name, node_modules_dir)
    return f"""Package: {name}
Version: {version}
License: <license>
License Text:

{license_text if license_text else "<license text not found>"}
--------------------------------
"""


def write_license_file(lockfile: str, node_modules_dir: str) -> None:
    """
    Writes a license file with all packages.
    """
    with open("LICENSEALL.md", "w") as f:
        for package in split_lockfile(lockfile)[1:]:
            f.write(generate_license_text(package, node_modules_dir))




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path", help="Path to your project")
    args = parser.parse_args()
    
    # check if the project path is valid
    if not os.path.isdir(args.project_path):
        print("Invalid project path")
        sys.exit(1)

    # check if the project path has a yarn.lock file
    if not os.path.isfile(os.path.join(args.project_path, "yarn.lock")):
        print("No yarn.lock file found")
        sys.exit(1)

    # check if the project path has a node_modules directory
    if not os.path.isdir(os.path.join(args.project_path, "node_modules")):
        print("No node_modules directory found")
        sys.exit(1)

    # read in the lockfile
    with open(os.path.join(args.project_path, "yarn.lock"), "r") as f:
        lockfile = f.read()

    write_license_file(lockfile, os.path.join(args.project_path, "node_modules"))
