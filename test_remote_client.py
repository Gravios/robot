import socket

ip = "192.168.2.101"
timer = 0
# Main program loop:
while True:

    # Receive data
    if timer < 1:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((str(ip), 5000))
        data = client_socket.recv(1024).decode()
        timer = 30

    else:
        timer -= 1

    print(data)
