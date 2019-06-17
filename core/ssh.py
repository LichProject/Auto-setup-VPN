import os
import socket
from enum import Enum, auto

import paramiko
from paramiko import BadHostKeyException, AuthenticationException, SSHException

from config import vpn_data


class SSHResult(Enum):
    NONE = auto()
    BAD_HOST_KEY = auto()
    AUTHENTICATION_FAILED = auto()
    SSH_ERROR = auto()
    FTP_ERROR = auto()
    SOCKET_ERROR = auto()
    KEY_NOT_FOUND = auto()
    SCRIPT_NOT_FOUND = auto()
    EXECUTE_ERROR = auto()


class SSH:
    __script_file_path = "core/script.sh"
    __private_keys_directory = "private_keys"
    __remote_file_path = "/root/vpn.sh"
    __client = None

    def __init__(self, ip, user, password, rsa_key=None):
        self.ip = ip
        self.user = user
        self.password = password
        self.rsa_key = rsa_key

    @property
    def __get_private_key(self):
        return f"{self.__private_keys_directory}/{self.rsa_key}"

    def connect(self):
        pkey = None
        if self.rsa_key is not None:
            if not os.path.exists(self.__get_private_key):
                return SSHResult.KEY_NOT_FOUND
            pkey = paramiko.RSAKey.from_private_key_file(self.__get_private_key)  # Set RSA-key for the connect.
        self.__client = paramiko.SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if self.rsa_key is not None:
                self.__client.connect(self.ip, username=self.user, pkey=pkey)
            else:
                self.__client.connect(self.ip, username=self.user, password=self.password)
        except BadHostKeyException:
            return SSHResult.BAD_HOST_KEY
        except AuthenticationException:
            return SSHResult.AUTHENTICATION_FAILED
        except SSHException:
            return SSHResult.SSH_ERROR
        except socket.error:
            return SSHResult.SOCKET_ERROR
        return SSHResult.NONE

    def create_vpn_script(self):
        if self.__client is None:
            return SSHResult.SSH_ERROR
        if not os.path.exists(self.__script_file_path):
            print("Script not found: " + self.__script_file_path)
            return SSHResult.SCRIPT_NOT_FOUND
        with self.__client.open_sftp() as ftp:
            with open(self.__script_file_path, 'r', encoding='utf-8') as file:
                text = file.read() \
                    .replace("RESERVED_USER", vpn_data['user']) \
                    .replace("RESERVED_PASSWORD", vpn_data['password'])
            with ftp.file('vpn.sh', 'a', -1) as file:
                file.write(text)
        return SSHResult.NONE

    def execute(self):
        if self.__client is None:
            return SSHResult.SSH_ERROR
        ssh_stdin, ssh_stdout, ssh_stderr = self.__client.exec_command("sh vpn.sh")
        for line in iter(ssh_stdout.readline, ""):
            print(line, end="")
        return SSHResult.NONE
