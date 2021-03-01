from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ""
PORT = 8000

if __name__ == '__main__':
    HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()