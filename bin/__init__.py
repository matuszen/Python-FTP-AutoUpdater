from configparser import ConfigParser
from time import time
from bin.utility import *


def main():
    start = time()

    conf = ConfigParser()
    conf.read("../config.ini")

    host = conf.get("CONNECT", "host")
    port = (
        conf.getint("CONNECT", "port")
        if conf.get("CONNECT", "port").lower() != "default"
        else conf.get("CONNECT", "port").lower()
    )

    login = conf.get("USER", "login").strip()
    password = conf.get("USER", "password").strip()

    source_direction = conf.get("DIRECTORIES", "source_direction").strip()
    destination_direction = conf.get("DIRECTORIES", "destination_direction").strip()

    program_status = conf.get("SCRIPT SETTINGS", "program_status").strip().lower()
    disabled_elements = validate_tuple(conf.get("SCRIPT SETTINGS", "disabled_elements"))

    print()

    ftp = FTPconn(host, login, password, port)

    source_direction, destination_direction = ftp.validate_directories(
        source_direction, destination_direction
    )

    main_directory = str(source_direction).split(ftp.local_path_slash)[-1]
    main_path = f"{destination_direction}{ftp.remote_path_slash}{main_directory}"

    ftp.set_disabled_elements(disabled_elements)
    ftp.set_paths(source_direction, destination_direction, main_path, main_directory)

    os.chdir(source_direction)
    ftp.cd(destination_direction, send_command_only=True)

    log(f"Source direction: {source_direction}")
    log(f"Destination direction: {destination_direction}")

    if program_status == "update":
        ftp.check_main_directory()

        print()

        ftp.cd(main_directory, remote_path_only=True)

        try:
            ftp.check_file_structure()
        except Exception as e:
            log(f"{str(e)}\n")
            raise
        else:
            ftp.cd(destination_direction, send_command_only=True)
            log("Updating completed. No problems found")

    elif program_status == "delete":
        ftp.check_main_directory()

        print()

        try:
            ftp.clear_file_structure()
            try:
                ftp.rmdir(main_directory)
                log(f"Delete {main_directory}")
            except:
                pass

        except Exception as e:
            log(f"{str(e)}\n")
            raise

        else:
            ftp.cd(destination_direction, send_command_only=True)
            log("Delete completed. No problems found")

    # elif program_status == 'upload':
    #     ftp.check_main_directory()

    #     print()

    #     os.chdir(source_direction)
    #     ftp.cd(main_directory, remote_path_only = True)

    #     try:
    #         ftp.create_file_structure()

    #     except Exception as e:
    #         log(f'{str(e)}\n')
    #         raise

    #     else:
    #         ftp.cd(destination_direction, send_command_only = True)
    #         log('Transfer completed. No problems found')

    elif program_status == "test":
        log("Testing conection complete. No problems found")

    else:
        raise ValueError('Wrong "program_status" value in config.ini')

    print()

    ftp.close()

    end = time()

    log(f"Time taken: {round(end - start, 3)} s")

    print()


if __name__ == "__main__":
    main()
