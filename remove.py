from utility import *

def checkFileStructure(ftp: FTP, mainDir: str) -> FTP:
    """Searching through current working directory, to find files and delete them. After this, delete main folder

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib
    mainDir : str
        main dir in file structure, remove all elements in this folder

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    currentDir = analyzeDirectoryOnServer(ftp)

    if len(currentDir[1]) != 0:
        ftp = removeFiles(ftp, currentDir[1])

    for dir in currentDir[0]:
        ftp.cwd(dir)
        ftp = checkFileStructure(ftp, mainDir)
    

    destPath = ftp.pwd().split('/')
    ftp.cwd('/'.join(destPath[:-1]))

    if destPath[-1] == mainDir:
        return ftp

    ftp.rmd(destPath[-1])
    log(f'Delete {destPath[-1]}')

    return ftp


def removeFiles(ftp: FTP, files: list) -> FTP:
    """Remove files, in current working directory on server, which are listed in files param

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib
    files : list
        contains listed names of files (with extensions)

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    for file in files:
        ftp.delete(file)
        log(f'Delete {file}')

    return ftp


def analyzeDirectoryOnServer(ftp: FTP) -> tuple:
    """Analyzes current working directory, divides into folders and files, ignores git files

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib

    Returns
    -------
    tuple
        contains listed file and folder names, example: ([folders], [files])
    """

    dirElements = np.array(ftp.nlst(), dtype = str)

    folders = np.array([], dtype = str)
    files = np.array([], dtype = str)

    for element in dirElements:

        if element == '.git' or element == '.gitignore' or element == 'LICENSE' or element == '.' or element == '..' or element == '__pycache__':
            continue

        for char in element:
            if char == '.':
                break

        else:
            folders = np.append(folders, element)
            continue

        files = np.append(files, element)
    
    return (folders, files)
