#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 21:12:54 2021
@author: js-on
"""
from email.parser import Parser
from colorama import Fore
from typing import Any
import logging
import os.path
import glob
import os

logging.basicConfig(filename='3xtr4ct0r.l0g', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')
BASE_DIR = "Mailbox"


def motd():
    print(Fore.GREEN + " _____     _        _  _        _    ___       " + Fore.RESET)
    print(Fore.GREEN + "|___ /_  _| |_ _ __| || |   ___| |_ / _ \ _ __ " + Fore.RESET)
    print(Fore.GREEN + "  |_ \ \/ / __| '__| || |_ / __| __| | | | '__|" + Fore.RESET)
    print(Fore.GREEN + " ___) >  <| |_| |  |__   _| (__| |_| |_| | |   " + Fore.RESET)
    print(Fore.GREEN + "|____/_/\_\\__|_|     |_|  \___|\__|\___/|_| " + Fore.RESET)
    print(Fore.RED + "~ js-on (c) 2021")
    print()


def parse_message(filename: str) -> Any:
    """Read email content and create parsed email object

    Args:
        filename (str): path to eml file

    Returns:
        [Any]: email object
    """
    try:
        with open(filename) as f:
            return Parser().parse(f)
    except UnicodeDecodeError as e:
        logging.warning(repr(e))
        logging.warning(f'Decoding error in file \'{filename}\' ...')
        return None


def find_attachments(message: Parser) -> list:
    """Return a tuple of parsed content-disposition dict, message object
    for each attachment found.

    Args:
        message (Parser): parsed email message

    Returns:
        list: list of attachments
    """
    found = []
    for part in message.walk():
        if 'content-disposition' not in part:
            continue
        cdisp = part['content-disposition'].split(';')
        cdisp = [x.strip() for x in cdisp]
        if cdisp[0].lower() != 'attachment':
            continue
        parsed = {}
        for kv in cdisp[1:]:
            key, _, val = kv.partition('=')
            if val.startswith('"'):
                val = val.strip('"')
            elif val.startswith("'"):
                val = val.strip("'")
            parsed[key] = val
        found.append((parsed, part))
    return found


def run(eml_filename: str, output_dir: str) -> int:
    """run attachment extraction on email

    Args:
        eml_filename (str): path to eml file
        output_dir (str): path where to store the attachment

    Returns:
        int: amount of attachments
    """
    msg = parse_message(eml_filename)
    if not msg:
        return 0
    attachments = find_attachments(msg)
    for cdisp, part in attachments:
        cdisp_filename = eml_filename.replace(".", "_").replace(
            "/", "_") + "_" + os.path.normpath(cdisp['filename'])
        # prevent malicious crap
        if os.path.isabs(cdisp_filename):
            cdisp_filename = os.path.basename(cdisp_filename)
        towrite = os.path.join(output_dir, cdisp_filename)
        with open(towrite, 'wb') as fp:
            data = part.get_payload(decode=True)
            fp.write(data)
    return len(attachments)


def main():
    """Main function, iterate on all existing files in the Mailbox subdir
    """
    if not os.path.exists("Attachments"):
        os.mkdir("Attachments")
    FOLDERS = glob.glob(f"{BASE_DIR}/INBOX*")
    FOLDERS_CNT = len(FOLDERS)
    ATT_CNT = 0
    for i in range(FOLDERS_CNT):
        folder = FOLDERS[i]
        FILES = glob.glob(f"{folder}/*.eml")
        FILES_CNT = len(FILES)
        for j in range(FILES_CNT):
            file = FILES[j]
            print(
                f"Progress: Folder {i+1}/{FOLDERS_CNT} | File {j+1}/{FILES_CNT} | {ATT_CNT} attachments         ", end='\r')
            ATT_CNT += run(file, "Attachments")


if __name__ == '__main__':
    motd()
    main()
    exit(0)
