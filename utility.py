from datetime import datetime
from ftplib import FTP, FTP_TLS
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


def connect(host: str, user: str, password: str, protocole: str, port: int | str = 'default', useTLS: bool = False) -> FTP:
    """Starts and supports connection via FTP protocole

    Parameters
    ----------
    host : str
        the address of the server to which to connect
    user : str
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
        the object containing the entire connection to the server"""

    if host == '':
        log('Wrong parameters')
        raise ValueError('Please type host address in `config.ini`')

    passwdHash = "*" * len(password)

    log('Starting connection')
    log(f'Host: {host}')

    if port == 'default':
        port = 21
    else:
        port = int(port)

    return useFTP(host, user, password, port, passwdHash, useTLS=useTLS)


def useFTP(server: str, login: str, passwd: str, port: int, passwdHash: str, useTLS: bool) -> FTP:
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

    if useTLS:
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
