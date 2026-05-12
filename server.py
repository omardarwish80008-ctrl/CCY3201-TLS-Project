import ssl
import socket

def start_server():
    server_address = '0.0.0.0'
    server_port = 9443

    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    tls_context.keylog_filename = '/home/server/tls/sslkeys.log'
    tls_context.load_cert_chain(
        certfile='/home/server/tls/server/server.crt',
        keyfile='/home/server/tls/server/server.key'
    )
    tls_context.load_verify_locations('/home/server/tls/ca/ca.crt')

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((server_address, server_port))
    server_sock.listen(1)
    print(f"TLS Server started - Listening on {server_address}:{server_port}")

    secure_server = tls_context.wrap_socket(server_sock, server_side=True)
    client_conn, client_addr = secure_server.accept()
    print(f"New connection from: {client_addr}")

    http_request = client_conn.recv(4096).decode()
    print(f"Request:\n{http_request}")

    body = "<html><body><h1>Hello! TLS is working!</h1><p>Omar Darwish - CCY3201</p></body></html>"
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\n\r\n{body}"

    client_conn.sendall(response.encode())
    client_conn.close()
    print("Response sent. Connection closed.")

start_server()
