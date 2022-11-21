from functions import *
from globals import currentPath

def main():
    
    with open('config.ini', 'r') as file:
        data = file.readlines()
        file.close()

    server = data[0].split('=')[1].strip()
    sshFTP = data[1].split('=')[1].strip()
    port = data[2].split('=')[0].strip()
    login = data[3].split('=')[1].strip()
    passwd = data[4].split('=')[1].strip()
    originPath = Path(data[5].split('=')[1].strip())
    desinationPath = data[6].split('=')[1].strip()

    ftp = conn(server, login, passwd, ssh = bool(sshFTP))

    ftp.cwd(desinationPath)

    try:
        ftp.rmd('Autonomy')
    except:
        pass
    else:
        ftp.mkd('Autonomy')

    chdir(originPath)

    desinationPath = desinationPath + '/Autonomy'

    ftp.cwd(desinationPath)
    
    try:
        ftp = createFileStructure(ftp, originPath, desinationPath)
    except Exception as e:
        log(e)
    else:
        log('Transfer completed. No problems found')

    ftp.quit()


if __name__ == "__main__":
    main()
