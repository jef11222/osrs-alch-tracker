"""
Local Bridge HTTP Server for RuneLite / Microbot integration.
Listens for real-time events from AlchBridgePlugin.jar on 127.0.0.1:18833.
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class BridgeRequestHandler(BaseHTTPRequestHandler):
    # Quiet logger to avoid spamming stdout
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        if self.path == "/api/event":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                if content_len > 0:
                    raw_body = self.rfile.read(content_len)
                    data = json.loads(raw_body.decode("utf-8"))
                    # Dispatch to parent server callback
                    if hasattr(self.server, "event_callback") and self.server.event_callback:
                        self.server.event_callback(data)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                err_msg = json.dumps({"status": "error", "message": str(e)})
                self.wfile.write(err_msg.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path in ("/api/ping", "/api/status"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            items_count = len(getattr(self.server, "top_items", []))
            res = json.dumps({"status": "online", "service": "OSRS Alch Tracker Bridge", "top10_count": items_count})
            self.wfile.write(res.encode("utf-8"))
        elif self.path in ("/api/top10", "/api/recommendations"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            items = getattr(self.server, "top_items", [])
            self.wfile.write(json.dumps(items).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

class BridgeServer:
    def __init__(self, port=18833, event_callback=None):
        self.port = port
        self.event_callback = event_callback
        self.httpd = None
        self.thread = None
        self.is_running = False
        self.top_items = []

    def set_top_items(self, items):
        self.top_items = list(items or [])
        if self.httpd:
            self.httpd.top_items = self.top_items

    def start(self):
        try:
            self.httpd = HTTPServer(("127.0.0.1", self.port), BridgeRequestHandler)
            self.httpd.event_callback = self.event_callback
            self.httpd.top_items = self.top_items
            self.is_running = True
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            print(f"Bridge HTTP Server successfully started on 127.0.0.1:{self.port}")
            return True
        except Exception as e:
            print(f"Bridge Server failed to start on port {self.port}: {e}")
            self.is_running = False
            return False

    def stop(self):
        self.is_running = False
        if self.httpd:
            try:
                self.httpd.shutdown()
                self.httpd.server_close()
            except Exception:
                pass
            self.httpd = None
