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
    HOST, PORT, num_conns = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])


server_addr = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    while True:
        p_cpu = int(round(psutil.cpu_percent()))
        p_mem = int(round(psutil.virtual_memory()._asdict()['percent']))
        print ('cpu:', p_cpu, 'memory:', p_mem, end='\r', flush=True)
        buff = struct.pack('!ii', p_cpu, p_mem)
        sock.sendall(buff)
        time.sleep(0.4)

except KeyboardInterrupt:
    print('keyboard interruption detected')

def finalize():
    sock.close()

atexit.register(finalize)




