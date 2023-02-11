from datetime import datetime
from ftplib import FTP, FTP_TLS
import pysftp
from os import listdir, chdir, getcwd
from pathlib import Path
import numpy as np

def log(messege: str, showHour: bool = True) -> None:
    """Logs messege to console

    Parameters
    ----------
    messege : str
        messege, to be printed
    showHour : bool, optional
        determines whether to print a current hour, by default True
    """

    if showHour:
        now = datetime.now().strftime('%H:%M:%S')
        print(f'[{now}] {messege}')
    else:
        print(messege)


def conn(server: str, login: str, passwd: str, protocole: str, port: int = 'default', tls: bool = False, ssh: bool = False, atSign: bool = True) -> FTP:
    """Starts and supports connection via FTP or SFTP protocole

    Parameters
    ----------
    server : str
        the address of the server to which to connect
    login : str
        the login of the user to which to log in
    passwd : str
        user's passord
    port : int, optional
        custom port to use in connection, if empty, use default port
    tls : bool, optional
        use TLS to support and secure FTP communication, by default False
    ssh : bool, optional
        use SSH to support and secure SFTP communication, by default False

    Returns
    -------
    object
        the object containing the entire connection to the server
    """

    if server == '' or login == '':
        log('Wrong parameters')

    passwdHash = ''

    for char in range(len(passwd)):
        passwdHash += "*"
    
    if atSign:
        for char in range(len(login)):
            if char == "@":
                user = login
                break
        else:
            user = f'{login}@{server}'

    else:
        user = login

    log('Starting connection')
    log(f'Server: {server}')

    if protocole == 'FTP':

        if port == 'default':
            port = 21
        else:
            port = int(port)

        if tls == 'True':
            session = useFTP(server, user, passwd, port, passwdHash, tls = True)
        else:
            session = useFTP(server, user, passwd, port, passwdHash, tls = False)

    # elif protocole == 'SFTP':

    #     if port == 'default':
    #         port = 22
    #     else:
    #         port = int(port)

    #     session = useSFTP(server, login, passwd, port)

    return session


def useFTP(server: str, login: str, passwd: str, port: int, passwdHash: str, tls: bool) -> FTP:
    """Supports connection via FTP protocole

    Parameters
    ----------
    server : str
        the address of the server to which to connect
    login : str
        the login of the user to which to log in
    passwd : str
        user's passord
    port : int, optional
        custom port to use in connection, if empty, use default port
    tls : bool, optional
        use TLS to support and secure FTP communication, by default False

    Returns
    -------
    FTP
        the object containing the entire connection to the server. Create by ftplib
    """

    if tls:
        try:
            ftp = FTP_TLS()
            ftp.connect(server, port)
    
        except Exception as e:
            log(e)

        else:
            log(f'Succesfully connected to {server}')

        ftp.auth()
        log('Protocole: FTP (TLS support)')
        log(f'SSL version: {ftp.ssl_version}')

    else:
        try:
            ftp = FTP()
            ftp.connect(server, port)

        except Exception as e:
            log(e)

        else:
            log(f'Succesfully connected to {server}')

        log('Protocole: FTP')

    log(f'Port: {ftp.port}')
    ftp.encoding = 'utf-8'
    log('Encoding: UTF-8')

    try:
        log(f'User: {login}')
        log(f'Password: {passwdHash}')
        ftp.login(login, passwd)

    except:
        log('Login or password incorrect')
    
    else:
        log(f'Succesfully logged into {login}')
        log(ftp.getwelcome())
    
    return ftp


# def useSFTP(server: str, login: str, passwd: str, port: int = 'default') -> FTP:
#     """Supports connection via SFTP protocole

#     Parameters
#     ----------
#     server : str
#         the address of the server to which to connect
#     login : str
#         the login of the user to which to log in
#     passwd : str
#         user's passord
#     port : int, optional
#         custom port to use in connection, if empty, use default port

#     Returns
#     -------
#     FTP
#         the object containing the entire connection to the server. Create by pysftp
#     """

#     if server == '' or login == '':
#         log('Wrong parameters')
#         return None

#     passwdHash = ''

#     for char in range(len(passwd)):
#         passwdHash += "*"

#     for char in range(len(login)):
#         if char == "@":
#             user = login
#             break
#     else:
#         user = f'{login}@{server}'

#     log('Starting connection')
#     log(f'Server: {server}')

#     if tls == 'True':
#         try:
#             if port != 'default':
#                     ftp = FTP_TLS()
#                     ftp.connect(server, int(port))
#             else:
#                 ftp = FTP_TLS(server)
#         except Exception as e:
#             log(e)
#             return None
#         else:
#             log(f'Succesfully connected to {server}')

#         ftp.auth()
#         log('Protocole: FTP (TLS support)')
#         log(f'SSL version: {ftp.ssl_version}')

#     else:
#         try:
#             if port != 'default':
#                 ftp = FTP()
#                 ftp.connect(server, port)
#             else:
#                 ftp = FTP(server)
#         except Exception as e:
#             log(e)
#             return None
#         else:
#             log(f'Succesfully connected to {server}')

#         log('Protocole: FTP')

#     log(f'Port: {ftp.port}')
#     ftp.encoding = 'utf-8'
#     log('Encoding: UTF-8')

#     try:
#         log(f'User: {user}')
#         log(f'Password: {passwdHash}')
#         ftp.login(user, passwd)
#     except Exception as e:
#         log('Login or password incorrect')
#         return None
#     else:
#         log(f'Succesfully logged into {user}')
#         log(ftp.getwelcome())
    
#     return ftp
