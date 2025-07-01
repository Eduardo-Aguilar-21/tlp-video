import socket

ip = "192.168.10.242"
puertos = [554, 80, 8000, 8080, 8888, 8554, 5000, 37777, 49152, 9000]  # Puertos comunes en DVR
print(f"Escaneando {ip}...\n")

for puerto in puertos:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, puerto))
        print(f"✅ Puerto abierto: {puerto}")
        s.close()
    except:
        pass
 