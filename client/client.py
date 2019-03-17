import selectors
import socket
import struct
import sys
import types
import time
import psutil
import atexit

sel = selectors.DefaultSelector()

def now():
    return datetime.datetime.now()

if len(sys.argv) != 3:
    HOST = '192.168.0.113'
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
else:
    HOST, PORT = sys.argv[1], int(sys.argv[2])


server_addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    while True:
        p_cpu = psutil.cpu_percent()
        p_mem = psutil.virtual_memory()._asdict()['percent']
        print ('cpu: {0:.1f}'.format(p_cpu), 'memory: {0:.1f}'.format(p_mem), end='\r', flush=True)
        buff = struct.pack('!ff', p_cpu, p_mem)
        sock.sendall(buff)
        time.sleep(0.2)

except KeyboardInterrupt:
    print('keyboard interruption detected')

def finalize():
    sock.close()

atexit.register(finalize)




