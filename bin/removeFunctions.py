from utilitiesFunctions import *

def checkFileStructure(ftp: FTP, mainDir: str) -> FTP:

    currentDir = analyzeDirectory(ftp.nlst())

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
