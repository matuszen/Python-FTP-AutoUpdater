from datetime import datetime
from pathlib import Path
from ftplib import FTP
import numpy as np
import sys
import os


def log(messege: str, show_hour: bool = True) -> None:
    """Logs messege to console

    Parameters
    ----------
    messege : str
        messege, to be printed
    show_hour : bool, optional
        determines whether to print a current hour, by default True"""

    if show_hour:
        time = datetime.now().strftime("%H:%M:%S")
        sys.stdout.write(f"[{time}] {messege}")
    else:
        sys.stdout.write(messege)


def validate_tuple(element: str, elements_type: type = str) -> tuple:
    if elements_type == str:
        elements_type = lambda x: str(x)

    elif elements_type == int:
        elements_type = lambda x: int(x)

    elif elements_type == float:
        elements_type = lambda x: float(x)

    element = element.replace(" ", "")

    if element == "()" or len(element) == 0:
        return tuple()

    elif element[0] == "(" and element[-1] == ")":
        new_element = element[1:-1].split(",")
        for i in range(len(new_element)):
            new_element[i] = elements_type(new_element[i])
        return tuple(new_element)

    else:
        new_element = element.split(",")
        for i in range(len(new_element)):
            new_element[i] = elements_type(new_element[i])
        return tuple(new_element)


class FTPconn:
    def __init__(self, host: str, login: str, password: str, port: int = 21) -> None:
        """Initializes an FTP connection to the specified host, using the specified login credentials

        Parameters
        ----------
        host : str
            The hostname or IP address of the FTP server to connect to
        login : str
            The username to use for authentication
        password : str
            The plain text password to use for authentication
        port : int, optional
            The port number to use for the FTP connection, by default 21"""

        self.host, self.login, password, password_hash, self.port = self._validate_data(
            host, login, password, port
        )

        log("Starting connection")
        log(f"Host: {host}")

        self.conn = self._use_FTP(password, password_hash)

        self._check_path_styles()

        password = password_hash = ""
        del password, password_hash

    def _validate_data(self, host: str, login: str, password: str, port: int) -> tuple:
        """Validates the input parameters and returns them as a tuple

        Parameters
        ----------
        host : str
            The hostname or IP address to connect to
        login : str
            The username to use for authentication
        password : str
            The password to use for authentication
        port : int or str
            The port number to connect to. If "default", port 21 will be used

        Returns
        -------
        Tuple[str, str, str, str, int]
            A tuple containing validated values for `host`, `login`, `password`, `password_hash`, and `port`

        Raises
        ------
        ValueError
            If `host` is an empty string or consists only of whitespace characters"""

        port = int(port) if port != "default" else 21

        password_hash = "*" * len(password)

        if not host.strip():
            log("Wrong parameters")
            raise ValueError("Invalid host address provided in `config.ini`")

        if not isinstance(login, str):
            login = str(login)

        elif not isinstance(password, str):
            password = str(password)

        return host, login, password, password_hash, port

    def check_main_directory(self) -> None:
        try:
            self.nlst().index(self.main_directory)
        except ValueError:
            self.mkdir(self.main_directory)

    def validate_directories(
        self, source_direction: str, destination_direction: str
    ) -> tuple:
        if (
            source_direction.find(self.remote_path_slash) != -1
            or destination_direction.find(self.local_path_slash) != -1
        ):
            source_direction = source_direction.replace(
                self.remote_path_slash, self.local_path_slash
            )
            destination_direction = destination_direction.replace(
                self.local_path_slash, self.remote_path_slash
            )

        while source_direction[-1] == self.local_path_slash:
            source_direction = source_direction[0:-1]

        while destination_direction[-1] == self.remote_path_slash:
            destination_direction = destination_direction[0:-1]

        return source_direction, destination_direction

    def _use_FTP(self, password: str, password_hash: str) -> FTP:
        """Connects to an FTP server using the specified host, port, login, password, and encoding

        Parameters
        ----------
        password : str
            The plain text password to use for authentication
        password_hash : str
            The hashed password to use for authentication

        Returns
        -------
            An instance of the ftplib.FTP class representing the connected FTP server"""

        try:
            ftp = FTP()
            ftp.encoding = "UTF-8"

            log("Protocole: FTP")
            log(f"Port: {self.port}")
            log(f"Encoding: {ftp.encoding}")

            ftp.connect(self.host, self.port)

        except Exception as e:
            log(f"{str(e)}\n")
            raise

        else:
            log(f"Succesfully connected to {self.host}")

        try:
            log(f"User: {self.login}")
            log(f"Password: {password_hash}")
            ftp.login(self.login, password)

        except Exception as e:
            log(f"{str(e)}\n")
            raise

        else:
            log(f"Succesfully logged into {self.login}")
            log(ftp.getwelcome())

        return ftp

    def cd(
        self, path: str, remote_path_only: bool = False, send_command_only: bool = False
    ) -> None:
        """Change the current working directory on the FTP server and/or on the local machine

        Parameters
        ----------
        path : str
            The directory to change to, either a remote or local path
        remote_path_only : bool, optional
            If True, change only the remote working directory. Default is False
        send_command_only : bool, optional
            If True, send the change directory command to the FTP server, but do not change the local or remote working directory.
            Default is False"""

        if remote_path_only:
            try:
                self.conn.cwd(path)

            except:
                log(f"Failed to change directory to {path}")

            else:
                new_remote_path = f"{self.remote_path}{self.remote_path_slash}{path}"

                log(f"Change directory to {new_remote_path}")

                self.remote_path = new_remote_path

        elif send_command_only:
            self.conn.cwd(path)
            self.remote_path = self.cwd()

        else:
            try:
                self.conn.cwd(path)
                os.chdir(path)

            except:
                log(f"Failed to change directory to {path}")

            else:
                new_local_path = f"{str(self.local_path)}{self.local_path_slash}{path}"
                new_remote_path = f"{self.remote_path}{self.remote_path_slash}{path}"

                log(f"Change directory to {new_remote_path}")

                self.remote_path = new_remote_path
                self.local_path = new_local_path

    def cwd(self) -> str:
        """Return current working directory"""

        return self.conn.pwd()

    def nlst(self) -> list:
        """Return a list of files in a given directory"""

        return self.conn.nlst()

    def mkdir(self, directory_name: str) -> None:
        """Make a directory in current working directory

        Parameters
        ----------
        directory_name : str
            the name of the directory to be created"""

        self.conn.mkd(directory_name)

    def rmdir(self, directory_name: str) -> None:
        """Remove a directory in current working directory

        Parameters
        ----------
        directory_name : str
            the name of the directory to be removed"""

        self.conn.rmd(directory_name)

    def delete(self, file_name: str) -> None:
        """Remove a file in current working directory

        Parameters
        ----------
        file_name : str
            the name of the file to be removed"""

        self.conn.delete(file_name)

    def close(self) -> None:
        """Quit and close the connection"""

        self.conn.quit()

    def set_disabled_elements(self, disabled_elements: tuple) -> None:
        """Set the disabled elements to be used during uploading files

        Parameters
        ----------
        disabled_elements : tuple of str
            Representing the names od disabled elements"""

        self.disabled_elements = disabled_elements

    def set_paths(
        self, local_path: str, remote_path: str, main_path: str, main_directory: str
    ) -> None:
        """Set local and remote paths for FTP connection.

        Parameters:
        -----------
        local_path : str
            Local path to the directory that will be used as the root directory
            for file transfers. It should be an absolute path, otherwise it will
            be interpreted relative to the current working directory
        remote_path : str
            Remote path to the directory on the FTP server that will be used as
            the root directory for file transfers. It should be an absolute path,
            otherwise it will be interpreted relative to the FTP server's home
            directory
        main_path : str
            Main path to the directory containing the files to be uploaded
        main_directory : str
            Main directory containing the files to be uploaded"""

        self.local_path = local_path
        self.remote_path = remote_path
        self.main_path = main_path
        self.main_directory = main_directory

    def _check_path_styles(self) -> None:
        """Check the style of the remote and local paths"""

        self._check_remote_path_style()
        self._check_local_path_style()

    def _check_remote_path_style(self) -> None:
        """Check the style of the path used by the remote file system and set the `remote_path_style` and `remote_path_slash` attributes accordingly

        If the remote system is identified as running Windows, the `remote_path_style` attribute is set to `'NT'` and the `remote_path_slash` attribute is set to `'\\'`. If the remote system is identified as running a Unix-like system, the `remote_path_style` attribute is set to `'Posix'` and the `remote_path_slash` attribute is set to `'/'`. Otherwise, the `remote_path_style` attribute is set to `'Unknown'` and the `remote_path_slash` attribute is set to an empty string
        """

        try:
            response = self.conn.sendcmd("SYST")
            tokens = response.split()

            if len(tokens) > 1:
                system_type = tokens[1].upper()

                if system_type.startswith("WIN"):
                    self.remote_path_style = "NT"
                    self.remote_path_slash = "\\"

                elif system_type.startswith("UNIX"):
                    self.remote_path_style = "Posix"
                    self.remote_path_slash = "/"

                else:
                    self.remote_path_style = "Unknown"
                    self.remote_path_slash = ""

        except:
            self.remote_path_style = "Unknown"
            self.remote_path_slash = ""

    def _check_local_path_style(self) -> None:
        """Checks the local path style based on the operating system type. It sets the `local_path_style` attribute to the corresponding path style string (`'Posix'` or `'NT'`) and sets the `local_path_slash` attribute to the appropriate path separator. If the operating system is not recognized, it sets `local_path_style` to `'Unknown'` and `local_path_slash` to an empty string"""

        try:
            if os.name.lower() == "posix":
                self.local_path_style = "Posix"
                self.local_path_slash = "/"

            elif os.name.lower() == "nt":
                self.local_path_style = "NT"
                self.local_path_slash = "\\"

            else:
                self.local_path_style = "Unknown"
                self.local_path_slash = ""

        except:
            self.local_path_style = "Unknown"
            self.local_path_slash = ""

    def check_file_structure(self) -> None:
        """Checks the file structure between the local and remote directories. If the local directory
        contains more folders, it attempts to change the remote directory to match the local folder
        structure. If the remote directory doesn't contain a folder that exists in the local directory,
        it will move up one level until it reaches a directory that matches the local folder structure.
        Recursively calls itself for every local folder found"""

        local_folders, local_files = self._analyze_local_directory(
            os.listdir(self.local_path)
        )

        self._check_directory(local_folders, local_files)

        if len(local_folders) == 0:
            self._up_direction()

        else:
            for folder in local_folders:
                while not Path.exists(
                    Path(f"{self.local_path}{self.local_path_slash}{folder}")
                ):
                    self._up_direction()

                self.cd(folder)

                self.check_file_structure()

    def _up_direction(self) -> None:
        """Changing current working direction one level higher in file structure. Do this both on server, and on user comp"""

        local_path = self.local_path_slash.join(
            self.local_path.split(self.local_path_slash)[:-1]
        )
        remote_path = self.remote_path_slash.join(
            self.remote_path.split(self.remote_path_slash)[:-1]
        )

        os.chdir(local_path)
        self.cd(remote_path, send_command_only=True)

        self.local_path = local_path
        self.remote_path = remote_path

    def _check_directory(
        self, local_folders: np.ndarray, local_files: np.ndarray
    ) -> None:
        """Check the directory structure on the host and local system and synchronize them

        Parameters
        ----------
        local_folders : array of str
            An array of the folders in the local directory
        local_files : array of str
            An array of the files in the local directory"""

        self._create_folders(local_folders)
        self._upload_files(local_files)

        host_folders, host_files = self._analyze_host_directory()

        if not np.array_equal(host_files, local_files):
            self._check_files(host_files, local_files)

        if not np.array_equal(host_folders, local_folders):
            self._check_folders(host_folders, local_folders)

    def _create_folders(self, folders: np.ndarray) -> None:
        """Create folders on the remote host

        Parameters
        ----------
        folders : array of str
            An array of folder names to be created"""

        for folder in folders:
            try:
                self.mkdir(folder)
            except:
                log(f"Directory {folder} already exists")
            else:
                log(f"Create {folder} folder")

    def _upload_files(self, files: np.ndarray) -> None:
        """Uploads given files to the remote server. If a file with the same name already exists on the server, it is replaced

        Parameters
        ----------
        files : array of str
            An array of file names (with extensions) to be uploaded"""

        for file in files:
            try:
                self._send_file(file)
            except:
                self.delete(file)
                self._send_file(file)
                log(f"Replaced {file}")
            else:
                log(f"Upload {file}")

    def _send_file(self, file_name: str) -> None:
        """Uploads a file from the local directory to the remote FTP server

        Parameters
        ----------
        file_name : str
            The name of the file to be uploaded"""

        with open(f"{self.local_path}{self.local_path_slash}{file_name}", "rb") as file:
            self.conn.storbinary(f"STOR {file_name}", file)

    def _check_files(self, files_on_host: np.ndarray, local_files: np.ndarray) -> None:
        """This method checks the files on the remote host and deletes any files that do not exist locally

        Parameters
        ----------
        files_on_host : array of str
            An array containing the names of the files on the remote host
        local_files : array of str
             An array containing the names of the files locally"""

        for file in files_on_host:
            if file not in local_files:
                self.delete(file)
                log(f"Delete {file}")

    def _check_folders(
        self, folders_on_host: np.ndarray, local_folders: np.ndarray
    ) -> None:
        """Searches through folders on the remote host and compares them with local folders. If a folder is found on the host
        that is not in the local folder, the method changes the current working directory to that folder and recursively
        deletes its contents

        Parameters
        ----------
        folders_on_host : array of str
            Array containing the names of folders on the host.
        local_folders : array of str
            Array containing the names of local folders"""

        for folder in folders_on_host:
            if folder not in local_folders:
                self.cd(folder)
                self.clear_file_structure()

    def _is_directory(self, element_name: str) -> bool:
        """Checks if a given element on the remote server is a directory

        Parameters
        ----------
        element_name : str
            the name of the element to check

        Returns
        -------
        bool
            True if element is a directory, otherwise False"""

        current_directory = self.remote_path

        try:
            self.cd(element_name, send_command_only=True)
            self.cd(current_directory, send_command_only=True)
            return True

        except:
            return False

    def _analyze_local_directory(self, directory_elements: list) -> tuple:
        array_length = len(directory_elements)

        if array_length == 0:
            return [], []

        max_element_length = len(max(directory_elements, key=len))
        # local_folders = np.array([], dtype = str)
        # local_files = np.array([], dtype = str)
        local_folders = np.empty(array_length, dtype=f"U{max_element_length}")
        local_files = np.empty(array_length, dtype=f"U{max_element_length}")

        for element in directory_elements:
            if element not in self.disabled_elements:
                element_path = Path(
                    f"{self.local_path}{self.local_path_slash}{element}"
                )

                if element_path.is_dir():
                    # local_folders = np.append(local_folders, element)
                    local_folders[np.where(local_folders == "")[0][0]] = element

                else:
                    # local_files = np.append(local_files, element)
                    local_files[np.where(local_files == "")[0][0]] = element

        local_files = np.delete(local_files, np.where(local_files == "")[0])
        local_folders = np.delete(local_folders, np.where(local_folders == "")[0])

        return local_folders, local_files

    def _analyze_host_directory(self) -> tuple:
        """Analyze the contents of the current directory on an FTP server

        Returns
        -------
        tuple of two ndarrays
            A tuple containing a numpy array of folder names and a numpy array of file names.
            The folder and file names are represented as strings"""

        directory_elements = self.nlst()
        array_length = len(directory_elements)

        if array_length == 0:
            return [], []

        max_element_length = len(max(directory_elements, key=len))

        # remote_folders = np.array([], dtype = str)
        remote_folders = np.empty(array_length, dtype=f"U{max_element_length}")
        # remote_files = np.array([], dtype = str)
        remote_files = np.empty(array_length, dtype=f"U{max_element_length}")

        for element in directory_elements:
            if element in (".", ".."):
                continue

            elif self._is_directory(element):
                if element not in self.disabled_elements:
                    remote_folders[np.where(remote_folders == "")[0][0]] = element
                    # remote_folders: np.ndarray = np.append(remote_folders, element)

            else:
                if element not in self.disabled_elements:
                    remote_files[np.where(remote_files == "")[0][0]] = element
                    # remote_files: np.ndarray = np.append(remote_files, element)

        remote_files = np.delete(remote_files, np.where(remote_files == "")[0])
        remote_folders = np.delete(remote_folders, np.where(remote_folders == "")[0])

        return remote_folders, remote_files

    def clear_file_structure(self) -> None:
        """Recursively searches through the current working directory on the remote server and removes all files and folders"""

        remote_folders, remote_files = self._analyze_host_directory()

        current_directory = self.remote_path.split(self.remote_path_slash)[-1]

        if (
            self.remote_path == self.main_path
            and len((remote_files, remote_folders)) == 0
        ):
            return

        if len(remote_files) != 0:
            self._remove_files(remote_files)

        if len(remote_folders) == 0:
            self._up_direction()
            self._delete_main_directory(current_directory)
            return

        for folder in remote_folders:
            self.cd(folder)
            self.clear_file_structure()

        self._up_direction()

        self._delete_main_directory(current_directory)

    def _delete_main_directory(self, directory_name: list) -> None:
        """Delete the main directory on the FTP server

        Parameters
        ----------
        ftp : FTP
            FTP connection instance
        destPath : list of strings
            represent the path to the main directory to be deleted

        Returns
        -------
        FTP
            FTP connection instance after the main directory has been deleted"""

        self.rmdir(directory_name)
        log(f"Delete {directory_name}")

    def _remove_files(self, files: list) -> None:
        """Remove files, in current working directory on server, which are listed in files param

        Parameters
        ----------
        ftp : FTP
            the object containing the entire connection to the server. Create by ftplib
        files : list
            contains listed names of files (with extensions)

        Returns
        -------
        FTP
            the object containing the entire connection to the server. Create by ftplib
        """

        for file in files:
            try:
                self.delete(file)
                log(f"Delete {file}")
            except:
                log(
                    f"Failed to delete {self.remote_path}{self.remote_path_slash}{file}"
                )
                raise

    def create_file_structure(self) -> None:
        """This function creates a directory structure on an FTP server based on the local directory structure. If a directory or file already exists on the server, it will not be created again. The disabledElements parameter is a tuple containing the names of any files or folders that should be excluded from the upload

        Parameters
        ----------
        ftp : FTP
            an FTP object representing the connection to the server
        disabledElements : tuple of strings
            containing the names of any files or folders that should be excluded from the upload

        Returns
        -------
        FTP
            object representing the connection to the server"""

        folders, files = self._analyze_local_directory(os.listdir(self.local_path))

        self._create_directory(folders, files)

        if len(folders) == 0:
            self._up_direction()
            return

        else:
            for folder in folders:
                while not Path.exists(
                    Path(f"{self.local_path}{self.local_path_slash}{folder}")
                ):
                    self._up_direction()

                self.cd(folder)
                # os.chdir(Path(f'{Path.cwd()}\\{folder}'))

                self.create_file_structure()

    def _create_directory(self, folders: np.ndarray, files: np.ndarray) -> None:
        """Create folders and files in current working directory on server

        Parameters
        ----------
        ftp : FTP
            the object containing the entire connection to the server. Create by ftplib
        content : tuple
            contains listed files and dirs, ex: ([folders], [files])

        Returns
        -------
        FTP
            the object containing the entire connection to the server. Create by ftplib
        """

        self._create_folders(folders)
        self._upload_files(files)
