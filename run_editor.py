# -*- coding: utf-8 -*-
"""Schedule Editor launcher: serves the embedded editor locally and opens it
in an Edge app-mode window (chromeless). Downloads / PowerPoint export work
because it runs in a real browser engine."""
import http.server, socketserver, threading, sys, os, subprocess, socket, time, tempfile

def resource_path(rel):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)

with open(resource_path("Schedule_Editor_EN.html"), "rb") as f:
    HTML = f.read()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(HTML)
    def log_message(self, *a):
        pass

def pick_port():
    for p in (8123, 8124, 8137, 8199):
        try:
            s = socket.socket(); s.bind(("127.0.0.1", p)); s.close(); return p
        except OSError:
            continue
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

def find_edge():
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"):
        if os.path.exists(p):
            return p
    return None

def main():
    port = pick_port()
    httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/"

    if os.environ.get("SCHED_SELFTEST") == "1":
        import urllib.request
        data = urllib.request.urlopen(url).read()
        ok = (b"PptxGenJS=function" in data) and (b"function saveHTML()" in data)
        print("SELFTEST served=%d ok=%s" % (len(data), ok))
        httpd.shutdown()
        sys.exit(0 if ok else 1)

    print("=" * 52)
    print("  Schedule Editor  -  running")
    print("  " + url)
    print("=" * 52)

    edge = find_edge()
    if edge:
        profile = os.path.join(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()), "ScheduleEditorApp")
        proc = subprocess.Popen([edge, f"--app={url}", f"--user-data-dir={profile}",
                                 "--no-first-run", "--new-window"])
        print("  앱 창을 닫으면 자동 종료됩니다.")
        print("  (Close the app window to quit.)")
        try:
            proc.wait()
        except KeyboardInterrupt:
            pass
    else:
        import webbrowser
        webbrowser.open(url)
        print("  Edge를 찾지 못해 기본 브라우저로 열었습니다.")
        print("  이 창을 닫으면 종료됩니다. (Close this window to quit.)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    try:
        httpd.shutdown()
    except Exception:
        pass

if __name__ == "__main__":
    main()
