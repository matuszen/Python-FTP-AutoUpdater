# Python-FTP-File-AutoUpdater

This project is a script that performs various operations on a remote FTP server based on the configurations provided in the config.ini file.

## Prerequisites

- Python >= 3.7.x
- NumPy >= 1.13

## Installation

To use this project, follow these steps:

1. Clone the repository to your local machine.

   ```shell
   git clone https://github.com/matuszen/Python-FTP-File-AutoUpdater.git
   ```

2. Install the required dependencies by running the following command:

   ```shell
   pip install -r requirements.txt
   ```

Configure the `config.ini` file with the appropriate settings for your FTP server and desired operations.

## Configuration

The script uses the `config.ini` file to obtain the necessary configurations. Here's an overview of the sections and options in the file:

### CONNECT

- host: The hostname or IP address of the FTP server.
- port: The port number to connect to. Use "default" to use the default FTP port.

### USER

- login: The login username for the FTP server.
- password: The password for the FTP server.

### DIRECTORIES

- source_direction: The local directory path for the source files.
- destination_direction: The remote directory path for the destination files.

### SCRIPT SETTINGS

- program_status: The program status that determines the operation to perform. It can have the following values:

  - update: Updates the files on the FTP server according to the file structure in the source directory.
  - delete: Deletes the files and directories on the FTP server according to the file structure in the source directory.
  - test: Tests the connection to the FTP server.

- disabled_elements: A comma-separated list of elements (files or directories) that should be excluded from the operations. This option is only applicable for the update and delete program statuses.

## To config ftp on host

### Install vsftpd

```shell
sudo apt-get install vsftpd
```

### Edit vsftpd.conf

```shell
sudo nano /etc/vsftpd.conf
```

### Restart service

```shell
sudo service vsftpd restart
```

### Settings in /etc/vsftpd.conf

```shell
listen=NO
listen_ipv6=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
ftpd_banner=Welcome to blah FTP service
ls_recurse_enable=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
ssl_enable=NO
utf8_filesystem=YES
```

All other setting must be comment

## Contributing

Contributions to this project are welcome. Here are some ways you can contribute:

- Report bugs or suggest features by opening an issue.
- Submit your own improvements to the project by creating a pull request.

When contributing to this repository, please first discuss the change you wish to make via the issue tracker before making a pull request.

## License

Thi project is under MIT License
