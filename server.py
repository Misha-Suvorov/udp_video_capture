import cv2
import socket
import numpy as np
import base64


BUFF_SIZE = 65536
#BUFF_SIZE = 131072

# Set up the UDP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = "127.0.0.1"
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)

# Open video capture device
vid = cv2.VideoCapture(1)  # Use 0 for webcam

# Keep track of client addresses
clients = []

while True:
    # Receive a connection request
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    if client_addr not in clients:
        clients.append(client_addr)
        print('GOT connection from ', client_addr)
    else:
        print("lost connection")

    # Start streaming video to connected clients
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        # Encode the frame as JPEG
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 30])
        message = base64.b64encode(buffer)
        #print(len(message))

        # Send the message in chunks if necessary
        max_packet_size = 65507  # UDP max size
        for client_addr in clients:
            for i in range(0, len(message), max_packet_size):
                server_socket.sendto(message[i:i + max_packet_size], client_addr)
                server_socket.sendto(b'--END--', client_addr)#idicate end of frame



# Clean up
vid.release()
cv2.destroyAllWindows()
