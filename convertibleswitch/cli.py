"""Sets the system mode."""

from argparse import ArgumentParser, Namespace
from asyncio import subprocess
from subprocess import DEVNULL
from subprocess import CalledProcessError
from subprocess import CompletedProcess
from subprocess import check_call
from subprocess import run, check_output
from os import environ, execv, system
import sys
import re
from typing import Optional
from convertibleswitch.config import load_config

DESCRIPTION = "Switches a convertible device between modes"
SUDO = "/usr/bin/sudo"


def settings_setup():
    device_data = map(lambda entry: entry.split(":"), check_output(
        "sudo libinput list-devices | grep \"Device:\\|Capabilities:\\|Kernel:\"",
        shell=True, text=True).split("\n")[:-1])
    link_map_raw = check_output("""for device in `ls /dev/input/by-path`
    do echo \"/dev/input/by-path/$device|$(readlink -f /dev/input/by-path/$device)\"
    done""", shell=True, text=True).split("\n")[:-1]
    link_map = {}
    for link_raw in link_map_raw:
        parts = link_raw.split("|")
        link_map[parts[1]] = parts[0]
    devices = [{}]
    # Assign fields to devices
    for entry in device_data:
        try:
            devices[-1][entry[0].lower()]
            # Add link map to constructed device (if available)
            try: 
                devices[-1]["path"] = link_map[devices[-1]["kernel"]]
            except KeyError:
                devices[-1]["path"] = None
            # Add next device
            devices.append({})
        except KeyError:
            devices[-1][entry[0].lower()] = entry[1].strip()
    pass


modes = {
    None: lambda: "",
    "init": settings_setup
}


def get_args() -> Namespace:
    """Returns the CLI arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-n', '--notify', action='store_true',
        help='display an on-screen notification')
    subparsers = parser.add_subparsers(dest='mode')
    subparsers.add_parser('init', help='initialise')
    subparsers.add_parser('toggle', help='toggles the system mode')
    subparsers.add_parser('laptop', help='switch to laptop mode')
    subparsers.add_parser('tablet', help='switch to tablet mode')
    return parser.parse_args()


def main() -> None:
    """Runs the main program."""
    args = get_args()

    config = load_config()
    sudo = config.get('sudo', SUDO)
    notify = config.get('notify', False)

    # If not root - elevate
    if environ.get("USER") != "root":
        return system(f"{sudo} {' '.join(sys.orig_argv)}")

    modes[args.mode]()

    print()
