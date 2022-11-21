from datetime import datetime
from ftplib import FTP
from os import listdir
import os.path 
import numpy as np
from globals import currentPath

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
        use SFTP protocole, secured version os FTP, by default False

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
        ftp = FTP(server)
        ftp.encoding = 'utf-8'
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


def createFileStructure(ftp: FTP) -> FTP:

    globals = currentPath()
    
    try:
        originPathList = listdir(globals.origin)
    except NotADirectoryError:
        newPath = globals.dest.split('/')[:-1]
        destPath = '/'.join(newPath)
        newPath = globals.origin.split('/')[:-1]
        globals.origin = '/'.join(newPath)
        ftp.cwd(globals.dest)
        return ftp
        

    currentDirectory = analyzeDirectory(originPathList)

    ftp = makeDirectory(ftp, currentDirectory, globals.origin)

    log(ftp.nlst())

    if len(currentDirectory[0]) == 0:
        newPath = globals.dest.split('/')[:-1]
        destPath = '/'.join(newPath)
        newPath = globals.origin.split('/')[:-1]
        globals.origin = '/'.join(newPath)
        ftp.cwd(globals.dest)
        return ftp

    for dir in currentDirectory[0]:
        ftp.cwd(dir)
        globals.dest = ftp.pwd()
        log(globals.origin)
        log(f'Go to {globals.dest}')
        ftp = createFileStructure(ftp)

    return ftp


def makeDirectory(ftp: FTP, content: tuple, originPath: str) -> FTP:
    ftp = createFolders(ftp, content[0])
    ftp = uploadFiles(ftp, content[1], originPath)

    return ftp


def createFolders(ftp: FTP, folders: list) -> FTP:

    for folder in folders:
        ftp.mkd(folder)
        log(f'Create {folder} folder')
    
    return ftp


def uploadFiles(ftp: FTP, files: list, originPath: str) -> FTP:

    for file in files:
        with open(f'{originPath}/{file}', 'rb') as f:
            ftp.storbinary(f'STOR {file}', f)
            log(f'Upload {file}')
    
    return ftp


def analyzeDirectory(directory: list) -> tuple:
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

    for element in directory:

        if element == '.git' or element == '.gitignore' or element == 'LICENSE':
            continue

        for char in element:
            if char == '.':
                break

        else:
            folders.append(element)
            continue

        files.append(element)
    
    return (folders, files)
