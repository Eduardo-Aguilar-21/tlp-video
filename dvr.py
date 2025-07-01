import socket

IP = "192.168.10.242"
PUERTO = 200
BUFFER_SIZE = 4096

comandos = {
    "RTSP OPTIONS": b"OPTIONS rtsp://%s:9000 RTSP/1.0\r\nCSeq: 1\r\n\r\n" % IP.encode(),
    "HTTP GET": b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % IP.encode()
}

for nombre, comando in comandos.items():
    print(f"\n=== Probar {nombre} ===")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((IP, PUERTO))
        s.sendall(comando)
        respuesta = s.recv(BUFFER_SIZE)
        if respuesta:
            print("Respuesta recibida:")
            print(respuesta.decode(errors='ignore'))
        else:
            print("Sin respuesta del DVR.")
        s.close()
    except Exception as e:
        print(f"Error durante {nombre}: {e}")
