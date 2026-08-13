from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os, webbrowser
root=Path(__file__).resolve().parent
os.chdir(root)
url='http://127.0.0.1:8000/'
print('ごみナビを起動します:',url)
print('終了するには Ctrl+C')
try:webbrowser.open(url)
except:pass
ThreadingHTTPServer(('127.0.0.1',8000),SimpleHTTPRequestHandler).serve_forever()
