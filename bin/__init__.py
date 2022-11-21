from functions import *

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
    destPath = data[6].split('=')[1].strip()
    mainDir = data[5].split('=')[1].strip().split('\\')[-1]

    ftp = conn(server, login, passwd, ssh = bool(sshFTP))

    ftp.cwd(destPath)

    try:
        ftp.mkd(mainDir)
    except:
        pass

    chdir(originPath)

    ftp.cwd(f'{ftp.pwd()}/{mainDir}')
    
    try:
        ftp = checkFileStructure(ftp)
    except Exception as e:
        log(e)
    else:
        log('Transfer completed. No problems found')

    ftp.quit()


if __name__ == "__main__":
    main()
