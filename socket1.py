import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 200))
server_socket.listen(1)
print("Escuchando en el puerto 200...")

conn, addr = server_socket.accept()
print(f"Conexión desde {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Recibido:", data.decode())

conn.close()
