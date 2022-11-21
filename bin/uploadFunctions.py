from utilitiesFunctions import *

def createFileStructure(ftp: FTP) -> FTP:

    currentDir = analyzeDirectory(listdir(Path.cwd()))

    ftp = createDirectory(ftp, currentDir)

    if len(currentDir[0]) == 0:

        ftp = upDirection(ftp)

        return ftp

    else:
        for i in range(len(currentDir[0])):

            dir = currentDir[0][i]

            while not Path.exists(Path(f'{Path.cwd()}\{dir}')):
                ftp = upDirection(ftp)

            ftp.cwd(dir)
            originPath = Path(f'{Path.cwd()}\{dir}')
            chdir(originPath)

            log(f'Change direction to {ftp.pwd()}')

            ftp = createFileStructure(ftp)

    return ftp


def upDirection(ftp: FTP) -> FTP:
    originPath = Path(Path.cwd().parent)
    chdir(originPath)

    destPath = ftp.pwd().split('/')[:-1]
    ftp.cwd('/'.join(destPath))

    return ftp


def createDirectory(ftp: FTP, content: tuple) -> FTP:
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
