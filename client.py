import ssl
import socket

def connect_to_server():
    server_ip = '192.168.35.131'
    server_port = 9443

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.load_cert_chain(
        certfile='/home/client/tls/client/client.crt',
        keyfile='/home/client/tls/client/client.key'
    )
    tls_context.load_verify_locations('/home/client/tls/client/ca.crt')
    tls_context.check_hostname = False

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_client = tls_context.wrap_socket(client_sock, server_side=False)
    secure_client.connect((server_ip, server_port))
    print(f"Connected to server {server_ip}:{server_port}")

    request = "GET / HTTP/1.1\r\nHost: 192.168.35.131\r\n\r\n"
    secure_client.sendall(request.encode())

    response = secure_client.recv(4096).decode()
    print(f"Server response:\n{response}")

    secure_client.close()

connect_to_server()
