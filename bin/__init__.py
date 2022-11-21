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
    originPath = data[5].split('=')[1].strip()
    desinationPath = data[6].split('=')[1].strip()

    ftp = conn(server, login, passwd, ssh = bool(sshFTP))

    ftp.cwd(desinationPath)

    # try:
    #     ftp.rmd('Autonomy')
    # except:
    #     pass
    # else:
    #     ftp.mkd('Autonomy')

    ftp.mkd('Autonomy')

    desinationPath = desinationPath + '/Autonomy'

    ftp.cwd(desinationPath)

    globals = currentPath()
    globals.origin = originPath
    globals.dest = desinationPath

    ftp = createFileStructure(ftp)

    print(ftp.dir())

    ftp.quit()


if __name__ == "__main__":
    main()
