import http.server
import socketserver
import subprocess
import webbrowser
import os
import time
import sys

PORT = 8000

class LabLauncherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/launch':
            print("🚀 Launching Streamlit simulation...")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status": "launching"}')
            
            # Launch streamlit in the background, headless to prevent duplicate browser tabs
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", "with_guide.py", "--server.headless=true"])
            return
        elif self.path == '/':
            self.path = '/polarization_explainer.html'
            
        return super().do_GET()

def start_server():
    # Change to the directory of this script to easily serve the HTML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), LabLauncherHandler) as httpd:
        print(f"✨ Serving Explainer at http://localhost:{PORT}")
        print("Opening in browser...")
        webbrowser.open(f"http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    start_server()
