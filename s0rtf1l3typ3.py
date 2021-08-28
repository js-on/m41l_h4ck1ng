#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 22:32:29 2021
@author: js-on
"""

from colorama import Fore
import hashlib
import magic
import shutil
import os

BASE_DIR = "Attachments"


def motd():
    print(Fore.GREEN + """.dP"Y8  dP"Yb  88""Yb 888888""" + Fore.RESET)
    print(Fore.GREEN + """`Ybo." dP   Yb 88__dP   88  """ + Fore.RESET)
    print(Fore.GREEN + """o.`Y8b Yb   dP 88"Yb    88  """ + Fore.RESET)
    print(Fore.GREEN + """8bodP'  YbodP  88  Yb   88  """ +
          Fore.YELLOW + "this shit..." + Fore.RESET)
    print(Fore.RED + "~ js-on (c) 2021")
    print()


def deduplicate():
    """Deduplicate all files in the given directory
    """
    FILES = os.listdir(os.path.join(os.getcwd(), BASE_DIR))
    FILES = [f"{BASE_DIR}/{file}" for file in FILES]
    FILES_CNT = len(FILES)
    HASHES = []

    for i in range(FILES_CNT):
        print(f"Deduplicate {i} of {FILES_CNT} files ...", end='\r')
        file = FILES[i]
        filehash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        if filehash not in HASHES:
            HASHES.append(filehash)
        else:
            os.unlink(file)
    print()


def sort_files():
    """Sort files based on their filetype into subdirs
    """
    FILES = os.listdir(os.path.join(os.getcwd(), BASE_DIR))
    FILES = [f"{BASE_DIR}/{file}" for file in FILES]
    FILES_CNT = len(FILES)

    for i in range(FILES_CNT):
        file = FILES[i]
        print(f"Copy file {i+1} of {FILES_CNT} ...", end='\r')
        ftype = magic.from_file(file).split(" ")[0]
        DIR = f"{BASE_DIR}/{ftype.upper()}"
        if DIR.endswith("ISO"):
            DIR = DIR.replace("ISO", "MEDIA")
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        shutil.move(file, DIR)
    print()


def main():
    deduplicate()
    sort_files()


if __name__ == '__main__':
    motd()
    main()
    exit(0)
