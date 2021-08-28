#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 12:36:48 2021
@author: js-on
"""

from colorama import Fore
import imaplib
import glob
import os

LOCAL_DIR = 'Mailbox'

# Download config
IMAP_SERVER = 'imap.example.com'
EMAIL_ACCOUNT = 'jane.doe@example.com'
EMAIL_PASSWORD = "1'm_J4n3.D0e"


def motd():
    print(Fore.GREEN + "                              .                                                      " + Fore.RESET)
    print(Fore.GREEN + "                             ,W                  i  .                                " + Fore.RESET)
    print(Fore.GREEN + "          ..       :        i##                 LE  Ef.                              " + Fore.RESET)
    print(Fore.GREEN + "         ,W,     .Et       f###    jt          L#E  E#Wi            :     :KW,      L" + Fore.RESET)
    print(Fore.GREEN + "        t##,    ,W#t      G####   G#t         G#W.  E#K#D:         G#j     ,#W:   ,KG" + Fore.RESET)
    print(Fore.GREEN + "       L###,   j###t    .K#Ki##   E#t        D#K.   E#t,E#f.     .E#G#G     ;#W. jWi " + Fore.RESET)
    print(Fore.GREEN + "     .E#j##,  G#fE#t   ,W#D.,##   E#t       E#K.    E#WEE##Wt   ,W#; ;#E.    i#KED.  " + Fore.RESET)
    print(Fore.GREEN + "    ;WW; ##,:K#i E#t  i##E,,i##,  E#t     .E#E.     E##Ei;;;;. i#K:   :WW:    L#W.   " + Fore.RESET)
    print(Fore.GREEN + "   j#E.  ##f#W,  E#t ;DDDDDDE##DGiE#t    .K#E       E#DWWt     :WW:   f#D.  .GKj#K.  " + Fore.RESET)
    print(Fore.GREEN + " .D#L    ###K:   E#t        ,##   E#t   .K#D        E#t f#K;    .E#; G#L   iWf  i#K. " + Fore.RESET)
    print(Fore.GREEN + ":K#t     ##D.    E#t        ,##   E#t  .W#G         E#Dfff##E,    G#K#j   LK:    t#E " + Fore.RESET)
    print(Fore.GREEN + "...      #G      ..         .E#   tf, :W##########WtjLLLLLLLLL;    j#;    i       tDj" + Fore.RESET)
    print(Fore.RED + "~ js-on (c) 2021" + Fore.RESET)
    print()


def mailbox_login(server: str, account: str, password: str) -> imaplib.IMAP4:
    """[summary]

    Args:
        server (str): IMAP server
        account (str): username / mail addr
        password (str): password

    Returns:
        imaplib.IMAP4: connection to IMAP server
    """
    M = imaplib.IMAP4(server)
    M.login(account, password)
    return M


def main():
    """login to mailbox and download all mails from the mailbox
    """
    M = mailbox_login(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD)
    folders = [folder.decode()[::-1].split('"." ')[0][::-1][1:].strip('"')
               for folder in M.list()[1]]
    for EMAIL_FOLDER in folders:
        if not os.path.exists(os.path.join(LOCAL_DIR, EMAIL_FOLDER)):
            os.mkdir(os.path.join(LOCAL_DIR, EMAIL_FOLDER))
        rv, data = M.select(EMAIL_FOLDER)
        if rv == 'OK':
            print(f'Downloading from: {LOCAL_DIR}/{EMAIL_FOLDER}')
            rv, data = M.search(None, 'ALL')
            if rv != 'OK':
                print('No messages found!')
                continue

            # confusing stuff to skip already downloaded mails
            # you can rerun the script and it'll start where it has crashed
            # and collects new mails for you as well
            try:
                add = max([int(i.split("/")[-1].split(".")[0])
                           for i in glob.glob(f"{LOCAL_DIR}/{EMAIL_FOLDER}/*.eml")])
            except Exception as e:
                print(repr(e))
                add = 0
            try:
                data_it = data[0].split()[add:]
            except:
                continue
            for num in data_it:
                rv, data = M.fetch(num, '(RFC822)')
                if rv != 'OK':
                    print(f'Error getting message {int(num)}')
                    continue
                fname = os.path.join(
                    LOCAL_DIR, f'{EMAIL_FOLDER}/{int(num)}.eml')
                print(f'Writing message {fname}', end='\r')
                with open(fname, 'wb') as f:
                    f.write(data[0][1])
        else:
            print(f'ERROR: Unable to open mailbox {repr(rv)}')
        print()
        try:
            M.close()
        except:
            pass
    M.logout()


if __name__ == '__main__':
    motd()
    main()
    exit(0)
