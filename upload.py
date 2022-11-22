from utility import *

def createFileStructure(ftp: FTP, disabledElements: tuple) -> FTP:
    """Creates file structure in current working directory

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    currentDir = analyzeDirectoryOnHost(np.array(listdir(Path.cwd()), dtype = str), disabledElements)

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

            ftp = createFileStructure(ftp, disabledElements)

    return ftp


def upDirection(ftp: FTP) -> FTP:
    """Changing current working direction one level higher in file structure. Do this both on server, and on user comp

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    originPath = Path(Path.cwd().parent)
    chdir(originPath)

    destPath = ftp.pwd().split('/')[:-1]
    ftp.cwd('/'.join(destPath))

    return ftp


def createDirectory(ftp: FTP, content: tuple) -> FTP:
    """Create folders and files in current working directory on server

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib
    content : tuple
        contains listed files and dirs, ex: ([folders], [files])

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    ftp = createFolders(ftp, content[0])
    ftp = uploadFiles(ftp, content[1])

    return ftp


def createFolders(ftp: FTP, folders: list) -> FTP:
    """Create folders in current working directory on server, which names are listed in folders param

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib
    folders : list
        contains listed dirs names 

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    for folder in folders:
        ftp.mkd(folder)
        log(f'Create {folder} folder')

    return ftp


def uploadFiles(ftp: FTP, files: list) -> FTP:
    """Upload files from current working directory to server, which names are listed in files param

    Parameters
    ----------
    ftp : FTP
        the object containing the entire connection to the server. Create by ftplib
    files : list
        contains listed files names (with extensions)

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    for file in files:

        with open(f'{Path.cwd()}\{file}', 'rb') as f:
            ftp.storbinary(f'STOR {file}', f)
            log(f'Upload {file}')
    
    return ftp


def analyzeDirectoryOnHost(dirElements: list, disabledElements: tuple) -> tuple:
    """Analyzes current working directory, divides into folders and files, ignores git files

    Parameters
    ----------
    directory : list
        contains elements in current working directory

    Returns
    -------
    tuple
        contains listed file and folder names, example: ([folders], [files])
    """

    folders = np.array([], dtype = str)
    files = np.array([], dtype = str)

    for element in dirElements:

        for exception in disabledElements:
            if element == exception:
                break
        else:
    
            elementPath = Path(f'{Path.cwd()}\{element}')

            if elementPath.is_dir():
                folders = np.append(folders, element)
            elif elementPath.is_file():
                files = np.append(files, element)
    
    return (folders, files)
