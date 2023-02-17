from utility import *
from upload import *
from remove import *
from configparser import ConfigParser


def main():

    conf = ConfigParser()
    conf.read('config.ini')

    host = str(conf['CONNECT']['host'])
    port = int(conf['CONNECT']['port']) if conf['CONNECT']['port'] != 'default' else str(conf['CONNECT']['port'])
    protocole = str(conf['CONNECT']['protocole'])
    useTLS = bool(conf['CONNECT']['useTLS'] == 'True')

    login = str(conf['USER']['login'])
    password = str(conf['USER']['password'])

    sourceDirection = Path(conf['DIRECTORIES']['sourceDirection'])
    destinationDirection = str(conf['DIRECTORIES']['destinationDirection'])

    programStatus = str(conf['SCRIPT SETTINGS']['programStatus'])
    isModuleInProject = bool(conf['SCRIPT SETTINGS']['isModuleInProject'] == 'True')
    locationInProject = Path(conf['SCRIPT SETTINGS']['locationInProject'])
    disabledElements = tuple(conf['SCRIPT SETTINGS']['disabledElements'].split(', '))

    ftp = connect(host, login, password, protocole, port, useTLS=useTLS)

    chdir(sourceDirection)

    ftp.cwd(destinationDirection)

    if isModuleInProject:

        sourceDirection = Path(f'{sourceDirection.cwd()}{locationInProject}')

        conf['DIRECTORIES']['sourceDirection'] = str(Path.cwd())

        with open(Path(f'{sourceDirection}/config.ini'), 'w') as file:
            conf.write(file)

    log(f'Source direction: {Path.cwd()}')

    mainDir = str(sourceDirection).split('\\')[-1]

    try:
        ftp.nlst().index(mainDir)
    except ValueError:
        programStatus == 'test'
        ftp.mkd(mainDir)

    if programStatus == 'all' or programStatus == 'delete':

        chdir(sourceDirection)

        ftp.cwd(f'{destinationDirection}/{mainDir}')

        log(f'Destination direction: {ftp.pwd()}')

        try:
            ftp = checkFileStructure(ftp, mainDir)
        except Exception as e:
            log(e)
        else:
            log('Delete completed. No problems found')
            log(f'Change direction to {ftp.pwd()}')

    if programStatus == 'all' or programStatus == 'upload':

        chdir(sourceDirection)
        ftp.cwd(f'{destinationDirection}/{mainDir}')

        try:
            ftp = createFileStructure(ftp, disabledElements)
        except Exception as e:
            log(e)
        else:
            log('Transfer completed. No problems found')

    ftp.quit()


if __name__ == "__main__":
    main()
