# ftpModule docs

## To config ftp on host

sudo apt-get install vsftpd
sudo nano /etc/vsftpd.conf
sudo service vsftpd restart

## Settings in /etc/vsftpd.conf

listen=NO
listen_ipv6=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
ftpd_banner=Welcome to blah FTP service.
ls_recurse_enable=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
ssl_enable=NO
utf8_filesystem=YES

All other setting must be comment
