import cv2
import numpy as np


udp_ip = "127.0.0.1"  # IP
udp_port = 5600       # Port

#udp_stream_url = "udp://localhost:1234"  # change to real URL
output_file = "output_video.mp4"  # out file

# open udp 
#cap = cv2.VideoCapture(1)
cap = sock = cv2.VideoCapture(f"udp://{udp_ip}:{udp_port}")


if not cap.isOpened():
    print("Не вдалося відкрити відео потік.")
    exit()

# getting information
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Налаштування для запису відео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Використовуємо кодек mp4v
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

while True:
    # Зчитуємо кадр з потоку
    ret, frame = cap.read()
    if not ret:
        break

    # Записуємо кадр у файл
    out.write(frame)

# Закриваємо відео потік і файл
cap.release()
out.release()
cv2.destroyAllWindows()

print("Відео успішно записано в файл", output_file)
