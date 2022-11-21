from utilitiesFunctions import *
from uploadFunctions import *
from removeFunctions import *


def main():
    
    with open('config.ini', 'r') as file:
        data = file.readlines()
        file.close()

    server = data[0].split('=')[1].strip()
    useTLS = data[1].split('=')[1].strip()
    port = data[2].split('=')[1].strip()
    login = data[3].split('=')[1].strip()
    passwd = data[4].split('=')[1].strip()
    originPath = Path(data[5].split('=')[1].strip())
    mainDir = data[5].split('=')[1].strip().split('\\')[-1]
    destPath = data[6].split('=')[1].strip()
    uploadOnly = data[7].split('=')[1].strip()
    deleteOnly = data[8].split('=')[1].strip()

    ftp = conn(server, login, passwd, port, tls = useTLS)

    ftp.cwd(destPath)

    try: 
        ftp.mkd(mainDir)
    except:
        pass

    if uploadOnly == 'False':

        chdir(originPath)
        ftp.cwd(f'{destPath}/{mainDir}')

        try:
            ftp = checkFileStructure(ftp, mainDir)
        except Exception as e:
            log(e)
        else:
            log('Delete completed. No problems found')

    if deleteOnly == 'False':

        chdir(originPath)
        ftp.cwd(f'{destPath}/{mainDir}')

        try:
            ftp = createFileStructure(ftp)
        except Exception as e:
            log(e)
        else:
            log('Transfer completed. No problems found')


    ftp.quit()


if __name__ == "__main__":
    main()
