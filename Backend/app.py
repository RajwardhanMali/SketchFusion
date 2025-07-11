import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 7860))  # Replace with correct IP and port
    print("Connected successfully!")
except ConnectionRefusedError as e:
    print(f"Connection error: {e}")
finally:
    s.close()
