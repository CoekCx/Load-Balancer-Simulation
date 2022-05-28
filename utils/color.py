import os
from enum import Enum


class Color(Enum):
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = ''
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def cursor():
    print_in_color('> ', Color.DARKCYAN, end='')


def print_in_color(text, color, bold=False, end='\n'):
    if bold:
        print(f'{Color.BOLD.value}{color.value}{text}{Color.END.value}', end=end)
    else:
        print(f'{color.value}{text}{Color.END.value}', end=end)


def in_color(text, color, bold=False):
    if bold:
        return f'{Color.BOLD.value}{color.value}{text}{Color.END.value}'
    else:
        return f'{color.value}{text}{Color.END.value}'


def print_error(text, clear_screen=True):
    if clear_screen:
        os.system('cls' if os.name == 'nt' else 'clear')
    print_in_color(text, Color.RED)
    cursor()
    input()


def print_message(text, clear_screen=False):
    if clear_screen:
        os.system('cls' if os.name == 'nt' else 'clear')
    print_in_color(text, Color.GREEN)
    cursor()
    input()
