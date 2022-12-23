from utility import *
from upload import *
from remove import *

def main():
    
    with open('./config.ini', 'r') as file:
        data = file.readlines()
        file.close()

    server = data[0].split('=')[1].strip()
    login = data[1].split('=')[1].strip()
    passwd = data[2].split('=')[1].strip()
    port = data[3].split('=')[1].strip()
    protocole = data[4].split('=')[1].strip()
    tls = data[5].split('=')[1].strip()
    atSign = data[6].split('=')[1].strip()
    originPath = Path(data[7].split('=')[1].strip())
    destPath = data[8].split('=')[1].strip()
    uploadOnly = data[9].split('=')[1].strip()
    deleteOnly = data[10].split('=')[1].strip()
    runOnly = data[11].split('=')[1].strip()
    isModuleInProject = data[12].split('=')[1].strip()
    locationInProject = data[13].split('=')[1].strip()
    disabledElements = tuple(data[14].split('=')[1].strip().split(', '))

    if atSign == 'True': atSign = True
    elif atSign == 'False': atSign = False

    ftp = conn(server, login, passwd, protocole, port, tls = tls, atSign = atSign)

    ftp.cwd(destPath)
    chdir(originPath)

    if isModuleInProject == 'True':

        originPath = Path(f'{Path(originPath.cwd())}{locationInProject}')
        
        with open('./config.ini', 'w') as file:
            data[5] = f'sourceDirection = {Path.cwd()}\n'
            file.writelines(data)
            file.close()
    
    log(f'Source direction: {Path.cwd()}')

    mainDir = str(originPath).split('\\')[-1]

    try:
        ftp.nlst().index(mainDir)
    except ValueError:
        uploadOnly == 'True'
        ftp.mkd(mainDir)

    if uploadOnly == 'False' and runOnly == 'False':

        chdir(originPath)

        ftp.cwd(f'{destPath}/{mainDir}')

        log(f'Destination direction: {ftp.pwd()}')

        try:
            ftp = checkFileStructure(ftp, mainDir)
            log(ftp.pwd())
        except Exception as e:
            log(e)
        else:
            log('Delete completed. No problems found')

    if deleteOnly == 'False' and runOnly == 'False':

        chdir(originPath)
        ftp.cwd(f'{destPath}/{mainDir}')

        try:
            ftp = createFileStructure(ftp, disabledElements)
        except Exception as e:
            log(e)
        else:
            log('Transfer completed. No problems found')


    ftp.quit()


if __name__ == "__main__":
    main()
