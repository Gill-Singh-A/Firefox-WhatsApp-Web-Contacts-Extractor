#! /usr/bin/env python3

import os, subprocess
from pathlib import Path
from datetime import date
from optparse import OptionParser
from colorama import Fore, Back, Style
from time import strftime, localtime

status_color = {
    '+': Fore.GREEN,
    '-': Fore.RED,
    '*': Fore.YELLOW,
    ':': Fore.CYAN,
    ' ': Fore.WHITE
}

folder_name = ".mozilla"
default_path = Path.home() / folder_name

def display(status, data, start='', end='\n'):
    print(f"{start}{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {strftime('%H:%M:%S', localtime())}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}", end=end)

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

def getContacts(file_path):
    strings = subprocess.check_output(["strings", file_path]).decode().split('\n')
    contacts = {}
    contacts_indexes = [[index, line.split(',')[1].split('@')[0].split('"')[1]] for index, line in enumerate(strings) if "contact" in line and "whatsapp" in line]
    for index, number in contacts_indexes:
        try:
            inner_index = 1
            while "4binarySyncData" not in strings[index+inner_index-1]:
                inner_index += 1
            contacts[number] = strings[index+inner_index].strip()
        except:
            contacts[number] = ''
    return contacts

if __name__ == "__main__":
    arguments = get_arguments(('-p', "--path", "path", f"Path to Firefox Cache Folder (Default={default_path})"),
                              ('-w', "--write", "write", "Write to File (Default=Current Date and Time)"))
    if not arguments.path:
        arguments.path = default_path
    if not os.path.isdir(arguments.path):
        display('-', f"No Directory as {Back.YELLOW}{arguments.path}{Back.RESET}")
        exit(0)
    if not arguments.write:
        arguments.write = f"{date.today()} {strftime('%H_%M_%S', localtime())}"
    paths = []
    for path, folders, files in os.walk(arguments.path):
        if "whatsapp" in path:
                paths.extend([f"{path}/{file}" for file in files if "sqlite" in file])
    contacts = {}
    for path in paths:
        contacts.update(getContacts(path))
    display('+', f"Total Contacts => {Back.MAGENTA}{len(contacts)}{Back.RESET}")
    print('\n'.join([f"* {Fore.CYAN}{contact}{Fore.RESET} : {Fore.BLUE}{name}{Fore.RESET}" for contact, name in contacts.items()]))