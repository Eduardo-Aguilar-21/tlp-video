from http.server import BaseHTTPRequestHandler, HTTPServer
import cv2
import numpy as np
import io

# IP = "0.0.0.0"  # Escucha en todas las interfaces de red
# PUERTO = 999 
IP = "192.168.10.242" 
PUERTO = 9000   # Cambia al puerto que usa el DVR
# PUERTO = 6602


class DVRStreamHandler(BaseHTTPRequestHandler):
    def do_POST(self):  # Algunos DVRs envían video por POST
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        self.procesar_video(data)
        self.send_response(200)
        self.end_headers()

    def do_GET(self):  # Si el DVR usa GET para enviar el stream
        self.send_response(200)
        self.end_headers()
        while True:
            data = self.rfile.read(1024)
            if not data:
                break
            self.procesar_video(data)

    def procesar_video(self, data):
        try:
            np_arr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Stream DVR", frame)
                cv2.waitKey(1)
        except Exception as e:
            print("Error procesando frame:", e)

server = HTTPServer((IP, PUERTO), DVRStreamHandler)
print(f"Servidor escuchando en {IP}:{PUERTO}...")
server.serve_forever()
