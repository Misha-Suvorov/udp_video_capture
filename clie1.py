#!/usr/bin/env python

from __future__ import division
import cv2
import numpy as np
import socket
import struct
from datetime import datetime

MAX_DGRAM = 2**16

def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] == 1:
            break

def main():
    """ Getting image udp frame &
    concate before decode and output image """
    
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 9999))
    dat = b''
    dump_buffer(s)

    # Generate filename with current date and time
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'output_{timestamp}.mp4'  # Changed to .avi

    # Variables for VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for XVID video
    out = None
    frame_size = None
    frame_rate = 30  # You can adjust the frame rate if needed
    
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
            
            # Set up VideoWriter once when the first frame is decoded
            if out is None:
                frame_size = (img.shape[1], img.shape[0])  # Set the frame size from the first frame
                out = cv2.VideoWriter(filename, fourcc, frame_rate, frame_size)
            
            # Write the frame to the output video file
            out.write(img)
            
            # Display the frame (optional)
            cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Reset the data buffer for the next frame
            dat = b''

    # Release resources
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
    s.close()

if __name__ == "__main__":
    main()
