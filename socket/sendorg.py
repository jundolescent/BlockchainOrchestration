from socket import *
import sys
import os

CHUNKSIZE = 1_000_000

ip = sys.argv[1]

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((ip,5000))
sock.listen(1)
materials = ['organizations', 'channel-artifacts', 'bin', 'configtx', 'system-genesis-block']
while True:
    print('Waiting for a client...')
    client,address = sock.accept()
    print(f'Client joined from {address}')
    with client:
        for folder in materials:
            for path,dirs,files in os.walk(folder):
                for file in files:
                    filename = os.path.join(path,file)
                    relpath = os.path.relpath(filename,'server')
                    filesize = os.path.getsize(filename)

                    print(f'Sending {relpath}')

                    with open(filename,'rb') as f:
                        client.sendall(relpath.encode() + b'\n')
                        client.sendall(str(filesize).encode() + b'\n')

                        # Send the file in chunks so large files can be handled.
                        while True:
                            data = f.read(CHUNKSIZE)
                            if not data: break
                            client.sendall(data)
        print('Done.')

    break