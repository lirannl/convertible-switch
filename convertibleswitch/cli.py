"""Sets the system mode."""

from argparse import ArgumentParser, Namespace
from genericpath import exists
import json
import os
from posixpath import basename, dirname
from os import environ, execv, execve, system
from pwd import getpwnam
import sys

user = getpwnam(environ.get("SUDO_USER") or environ.get("USER"))

DESCRIPTION = "Switches a convertible device between modes"

def settings_setup():
    newConfig = {}
    print("Enter devices from /sys/bus/drivers/ to be disabled, press enter to finish")
    print("Hint: look in /sys/bus/usb/drivers/usbhid")
    newConfig["devices"] = []
    while True: 
        line = sys.stdin.readline().rstrip()
        if (line != ""): newConfig['devices'].append(line)
        else: break
    print("Enter shell command to be run when tablet mode is activated, press enter to finish")
    newConfig["tablet_commands"] = []
    while True: 
        line = sys.stdin.readline().rstrip()
        if (line != ""): newConfig['tablet_commands'].append(line)
        else: break
    print("Enter shell command to be run when laptop mode is activated, press enter to finish")
    newConfig["laptop_commands"] = []
    while True: 
        line = sys.stdin.readline().rstrip()
        if (line != ""): newConfig['laptop_commands'].append(line)
        else: break
    with open("/etc/convertible_switch.json", "w+") as configFile:
        json.dump(newConfig, configFile)

def toggle_devices(kernel_action: str):
    with open("/etc/convertible_switch.json", "r") as configFile:
        config = json.load(configFile)
    devices = config.get("devices")
    for device in devices:
        open(f"{dirname(device)}/{kernel_action}", "w").write(basename(device))

def run_commands(entry: str):
    with open("/etc/convertible_switch.json", "r") as configFile:
        config = json.load(configFile)
    for command in config[entry]:
        system(command)

def is_laptop_mode():
    with open("/etc/convertible_switch.json", "r") as configFile:
        config = json.load(configFile)
    dev = config["devices"][0]
    return exists(f"{dev}/driver")

def switch_modes(force: str = ""):
    if (force == "tablet" or (is_laptop_mode() and force != "laptop")):
        toggle_devices("unbind")
        run_commands("tablet_commands")
    else:
        toggle_devices("bind")
        run_commands("laptop_commands")

modes = {
    None: lambda: "",
    "init": settings_setup,
    "tablet": lambda: switch_modes("laptop"),
    "laptop": lambda: switch_modes("tablet"),
    "toggle": switch_modes
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
    if os.getuid() != 0:
        execv("/usr/bin/sudo", ["/usr/bin/python"] + sys.orig_argv)
    args = get_args()
    with open("/etc/convertible_switch.json", "r") as configFile:
        config = json.load(configFile)

    try: 
        notify = config['notify'] 
    except KeyError:
        notify = False

    modes[args.mode]()

    pass
