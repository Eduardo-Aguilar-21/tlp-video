const http = require("http");
const WebSocket = require("ws");
const { spawn } = require("child_process");

const PORT_HTTP = 9000; // Puerto donde el DVR enviará el stream
const PORT_WS = 8002;   // Puerto WebSocket para los clientes

let clients = [];

// 🖥️ Servidor WebSocket para transmitir el video
const wss = new WebSocket.Server({ port: PORT_WS }, () => {
  console.log(`✅ Servidor WebRTC en ws://localhost:${PORT_WS}`);
});

wss.on("connection", (ws) => {
  clients.push(ws);
  console.log(`🔗 Cliente conectado. Total: ${clients.length}`);

  ws.on("close", () => {
    clients = clients.filter((client) => client !== ws);
    console.log(`❌ Cliente desconectado. Total: ${clients.length}`);
  });
});

// 📡 Servidor HTTP para recibir el video del DVR
const server = http.createServer((req, res) => {
  console.log("📡 Recibiendo stream del DVR...");

  req.on("data", (chunk) => {
    console.log(`📦 Recibidos ${chunk.length} bytes del DVR`);
  });

  req.on("end", () => {
    console.log("🚫 El DVR dejó de enviar datos.");
  });

  // ⚠️ Verifica que el DVR realmente envíe datos antes de lanzar FFmpeg
  const ffmpeg = spawn("ffmpeg", [
    "-i", "-",              // Entrada desde STDIN
    "-f", "mpegts",         // Formato de salida
    "-codec:v", "mpeg1video",
    "-b:v", "1000k",
    "-r", "25",
    "-"                     // Salida a STDOUT
  ]);

  ffmpeg.stdin.on("error", (err) => {
    console.error("❌ Error en FFmpeg stdin:", err.message);
  });

  req.pipe(ffmpeg.stdin); // 🔄 Conectar el stream del DVR a FFmpeg

  ffmpeg.stdout.on("data", (chunk) => {
    clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(chunk);
      }
    });
  });

  ffmpeg.stderr.on("data", (data) => {
    console.error("⚠️ FFmpeg Error:", data.toString());
  });

  ffmpeg.on("exit", (code, signal) => {
    console.log(`🚪 FFmpeg cerrado con código ${code} y señal ${signal}`);
  });

  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("OK"); // Confirma que el servidor HTTP recibió la solicitud
});

// Inicia el servidor HTTP
server.listen(PORT_HTTP, () => {
  console.log(`✅ Servidor HTTP escuchando en http://localhost:${PORT_HTTP}`);
});
