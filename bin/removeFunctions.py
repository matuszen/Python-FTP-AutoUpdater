from utilitiesFunctions import *

def checkFileStructure(ftp: FTP, mainDir: str) -> FTP:

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

    for file in files:
        ftp.delete(file)
        log(f'Delete {file}')

    return ftp

def analyzeDirectoryOnServer(ftp: FTP) -> tuple:
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

    dirElements = ftp.nlst()

    folders = []
    files = []

    for element in dirElements:

        if element == '.git' or element == '.gitignore' or element == 'LICENSE' or element == '.' or element == '..' or element == '__pycache__':
            continue

        for char in element:
            if char == '.':
                break

        else:
            folders.append(element)
            continue

        files.append(element)
    
    return (folders, files)
