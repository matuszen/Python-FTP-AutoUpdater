from datetime import datetime
from ftplib import FTP, FTP_TLS
from os import listdir, chdir
from pathlib import Path
import numpy as np

def log(messege: str, showHour: bool = True) -> None:
    """Logs messege to console

    Parameters
    ----------
    messege : str
        messege, to be printed
    showHour : bool, optional
        determines whether to print a current hour, by default True
    """

    if showHour:
        now =  datetime.now().strftime('%H:%M:%S')
        print(f'[{now}] {messege}')
    else:
        print(messege)


def conn(server: str, login: str, passwd: str, ssh: bool = False) -> FTP:
    """Supports connection via FTP protocole

    Parameters
    ----------
    server : str
        the address of the server to which to connect
    login : str
        the login of the user to which to log in
    passwd : str
        user's passord
    ssh : bool, optional
        use SFTP protocole, secured version of FTP, by default False

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    passwdHash = ''

    for char in range(len(passwd)):
        passwdHash += "*"

    for char in range(len(login)):
        if char == "@":
            user = login
            break
    else:
        user = f'{login}@{server}'

    log('Starting connection')

    try:
        log(f'Server: {server}')
        if ssh == 'True':
            ftp = FTP_TLS(server)
            ftp.auth()
            log('Protocole: SFTP')
            log(f'SSL version: {ftp.ssl_version}')
        else:
            ftp = FTP(server)
            log('Protocole: FTP')
        ftp.encoding = 'utf-8'
        log('Encoding: UTF-8')
    except Exception as e:
        log('Server connection failed')
        log(e)
        return None
    else:
        log(f'Succesfully connected to {server}')

    try:
        log(f'User: {user}')
        log(f'Password: {passwdHash}')
        ftp.login(user, passwd)
    except Exception as e:
        log('Authentication failed')
        log(e)
        return None
    else:
        log(f'Succesfully logged into {user}')
        log(ftp.getwelcome())
    
    return ftp


def analyzeDirectory(dirElements: list) -> tuple:
    """Analyzes indicated location, divides into folders and files, ignores git files

    Parameters
    ----------
    directory : list
        elements in given location

    Returns
    -------
    tuple
        example: ([folders], [files])
    """

    folders = []
    files = []

    for element in dirElements:

        if element == '.git' or element == '.gitignore' or element == 'LICENSE' or element == '.' or element == '..':
            continue

        for char in element:
            if char == '.':
                break

        else:
            folders.append(element)
            continue

        files.append(element)
    
    return (folders, files)
