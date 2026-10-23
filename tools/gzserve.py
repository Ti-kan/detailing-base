# Локальный сервер «как на хостинге»: gzip для HTML/CSS/JS и долгий кэш для картинок и шрифтов.
import sys, gzip, os, mimetypes
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
mimetypes.add_type("image/avif", ".avif"); mimetypes.add_type("font/woff2", ".woff2")
ROOT = sys.argv[2]
class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def log_message(self, *a): pass
    def do_GET(self):
        path = self.translate_path(self.path.split("?")[0])
        if os.path.isdir(path): path = os.path.join(path, "index.html")
        if not os.path.isfile(path):
            basename = os.path.basename(path)
            candidate = os.path.join(ROOT, basename)
            if os.path.isfile(candidate): path = candidate
        if not os.path.isfile(path): return super().do_GET()
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        file_size = os.path.getsize(path)
        range_header = self.headers.get("Range")
        
        if range_header and range_header.startswith("bytes="):
            try:
                parts = range_header[6:].split("-")
                start = int(parts[0]) if parts[0] else 0
                end = int(parts[1]) if parts[1] else file_size - 1
                end = min(end, file_size - 1)
                chunk_len = end - start + 1
                with open(path, "rb") as f:
                    f.seek(start)
                    chunk = f.read(chunk_len)
                self.send_response(206)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(chunk_len))
                self.send_header("Accept-Ranges", "bytes")
                if "/img/" in self.path or "/fonts/" in self.path: self.send_header("Cache-Control", "public, max-age=31536000, immutable")
                self.end_headers()
                self.wfile.write(chunk)
                return
            except (BrokenPipeError, ConnectionResetError):
                return
            except Exception:
                pass

        try:
            data = open(path, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text/") else ""))
            self.send_header("Accept-Ranges", "bytes")
            if (ctype.startswith("text/") or ctype in ("application/javascript", "image/svg+xml")) and "gzip" in self.headers.get("Accept-Encoding", ""):
                data = gzip.compress(data, 6)
                self.send_header("Content-Encoding", "gzip")
            if "/img/" in self.path or "/fonts/" in self.path: self.send_header("Cache-Control", "public, max-age=31536000, immutable")
            else: self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass
ThreadingHTTPServer.request_queue_size = 128
ThreadingHTTPServer(("0.0.0.0", int(sys.argv[1])), H).serve_forever()
