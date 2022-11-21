from datetime import datetime
from ftplib import FTP
from os import listdir, chdir, getcwd
from pathlib import Path
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


def createFileStructure(ftp: FTP, originPath: Path, destPath: str) -> FTP:
    
    originPathList = listdir(originPath)

    currentDirectory = analyzeDirectory(originPathList)

    ftp = makeDirectory(ftp, currentDirectory)

    if len(currentDirectory[0]) == 0:

        ftp = upDirection(ftp, originPath, destPath)

        return ftp

    else:
        for i in range(len(currentDirectory[0])):

            dir = currentDirectory[0][i]

            while not Path.exists(Path(f'{Path.cwd()}\{dir}')):
                ftp = upDirection(ftp, originPath, destPath)

            ftp.cwd(dir)
            destPath = ftp.pwd()
            originPath = Path(f'{Path.cwd()}\{dir}')
            chdir(originPath)

            log(f'Change direction to {originPath}')
            log(f'Upload to {destPath}')

            ftp = createFileStructure(ftp, originPath, destPath)

    return ftp


def upDirection(ftp: FTP, originPath: Path, destPath: str) -> FTP:
    originPath = Path(originPath.parent)
    chdir(originPath)

    newPath = destPath.split('/')[:-1]
    destPath = '/'.join(newPath)
    ftp.cwd(destPath)

    return ftp


def makeDirectory(ftp: FTP, content: tuple) -> FTP:
    ftp = createFolders(ftp, content[0])
    ftp = uploadFiles(ftp, content[1])

    return ftp


def createFolders(ftp: FTP, folders: list) -> FTP:

    for folder in folders:
        ftp.mkd(folder)
        log(f'Create {folder} folder')
    
    return ftp


def uploadFiles(ftp: FTP, files: list) -> FTP:

    for file in files:
        with open(f'{Path.cwd()}\{file}', 'rb') as f:
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
