import numpy as np
import cv2
import socket
import base64

BUFF_SIZE = 65507
udp_ip = "127.0.0.1"  # Server IP
udp_port = 9999       # Server Port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
client_socket.settimeout(10)  # Set timeout to handle network issues

# Send a connection message
message = b'Hello'
client_socket.sendto(message, (udp_ip, udp_port))

buffer = b""
out = None  # VideoWriter object (will be initialized later)

cv2.namedWindow('RECEIVING VIDEO', cv2.WINDOW_NORMAL)

while True:
    try:
        # Receive UDP packets and append them to the buffer
        packet, _ = client_socket.recvfrom(BUFF_SIZE)
        buffer += packet

        # Check if the buffer contains a complete frame (using delimiter)
        if b'--END--' in buffer:
            # Split the buffer into the frame and the remaining data
            frame_data, buffer = buffer.split(b'--END--')

            # Decode the frame
            try:
                if len(frame_data) > 0:  # Ensure the frame data is not empty
                    data = base64.b64decode(frame_data, validate=True)

                    if len(data) > 0:  # Ensure base64 decoding returns valid data
                        np_data = np.frombuffer(data, dtype=np.uint8)
                        
                        if np_data.size > 0:  # Ensure the buffer is not empty before decoding
                            frame = cv2.imdecode(np_data, 1)

                            if frame is not None:
                                # Initialize VideoWriter if needed
                                if out is None:
                                    frame_height, frame_width = frame.shape[:2]
                                    fourcc = cv2.VideoWriter_fourcc(*'X264')  # H.264 codec
                                    fps = 20.0  # Adjust FPS if needed
                                    output_filename = 'output.mp4'
                                    out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

                                # Display the frame
                                cv2.imshow("RECEIVING VIDEO", frame)

                                # Write the frame to the video file
                                out.write(frame)
                        else:
                            print("Empty frame data received")
                    else:
                        print("Base64 decoding returned no data")
                else:
                    print("Received an empty frame")

            except (base64.binascii.Error, cv2.error) as e:
                print(f"Error decoding frame: {e}")
                continue

    except socket.timeout:
        print("No data received, retrying...")

    # Press 'q' to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()
if out is not None:
    out.release()
cv2.destroyAllWindows()
