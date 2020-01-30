import socket
import ssl

with open("query.xml", "r") as f:
  packet = f.read().encode('utf-8')
  
HOST, PORT = 'testdrs.domain-REGISTRY.nl', 700

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(3)

wrappedSocket = ssl.wrap_socket(sock, keyfile='key.pem', certfile='certificate.pem')

# CONNECT AND PRINT REPLY
wrappedSocket.connect((HOST, PORT))
wrappedSocket.send(packet)
resp = wrappedSocket.recv(1280)
print(resp.decode())
# with open('result.xml', 'w') as f:
#   f.write(str(resp))

# CLOSE SOCKET CONNECTION
wrappedSocket.close()

# import subprocess
# subprocess.call(['perl', 'test.perl'])

# with open('result.xml', 'r') as f:
#   print(f.read())
