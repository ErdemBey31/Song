
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

PORT = 8000

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, world!')

httpd = TCPServer(("", PORT), MyHandler)
print("Web sunucusu çalışıyor...")
httpd.serve_forever()
