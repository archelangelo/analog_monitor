# analog_monitor
# server side, to be run on Raspberry Pi

import socket
import selectors
import sys
import types
import struct

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print ('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'')
    event_types = selectors.EVENT_READ
    sel.register(conn, event_types, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.inb += recv_data
        else:
            print ('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()

    if len(data.inb)>=8:
        p_cpu, p_mem = struct.unpack('!ff', data.inb[:8]) # percentages of cpu and mem usage
        data.inb = data.inb[8:]
        set_analog_output(p_cpu, p_mem)

def set_analog_output(p_cpu, p_mem):
    print ('cpu: {0:.1f}'.format(p_cpu), 'memory: {0:.1f}'.format(p_mem), end='\r', flush=True)
    pass

if len(sys.argv) != 3:
    HOST = '192.168.0.113'
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
else:
    HOST, PORT = sys.argv[1], int(sys.argv[2])

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print ('listening on', (HOST, PORT))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print ('caught keyboard interrupt, exiting')
finally:
    sel.close()
