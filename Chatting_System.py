import socket
import threading
import time

running = True

my_name = socket.gethostname()
my_address = socket.gethostbyname(my_name)
lis = my_address.split(sep='.')
network_address = lis[0] + '.' + lis[1] + '.' + lis[2]

connected_hosts = []

naming_port = 1200
naming_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
naming_socket.bind((my_address, naming_port))

messaging_port = 1201
messaging_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
messaging_socket.bind((my_address, messaging_port))

socket.setdefaulttimeout(1)


def ask_for_names():
    for i in range(1, 255):
        host_x = network_address + '.' + str(i)
        naming_socket.sendto("SendYourName".encode(), (host_x, naming_port))


def get_names_or_send_mine():
    while True:
        message, address = naming_socket.recvfrom(2048)
        message = message.decode()
        if message == "SendYourName":
            naming_socket.sendto(my_name.encode(), address)
        else:
            connected_hosts.append((message, address[0]))


def print_connected_hosts():
    for host_x in connected_hosts:
        print(host_x[0] + '@' + host_x[1])


def one_to_one_message(message, host_address):
    messaging_socket.sendto(message.encode(), (host_address, messaging_port))


def broadcast_message(message):
    messaging_socket.sendto(message.encode(), (network_address + '.' + '255', messaging_port))


def receive_messages():
    while True:
        message, address = messaging_socket.recvfrom(2048)
        message = message.decode()
        print("Received Message --->> ", message, "\nFrom --->> ", address[0])


# initial setup
thread1 = threading.Thread(target=get_names_or_send_mine)
thread2 = threading.Thread(target=receive_messages)
thread1.start()
thread2.start()

time.sleep(15)
ask_for_names()
time.sleep(15)


while running:
    print("\nPress '1' -> Print all connected hosts in the Network")
    print("Press '2' -> Send one-to-one message, enter the message and host IP")
    print("Press '3' -> Broadcast a message, enter the message")
    print("Press '0' -> Exit")

    option = input()
    option = int(option)

    if option == 1:
        print_connected_hosts()

    elif option == 2:
        print("Enter The Message:")
        msg = input()
        print("Enter The host IP")
        host = input()
        one_to_one_message(msg, host)

    elif option == 3:
        print("Enter The Message:")
        msg = input()
        broadcast_message(msg)

    else:
        running = 0

