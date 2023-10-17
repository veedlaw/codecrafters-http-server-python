import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")


    HOST = "localhost"
    PORT = 4221
    SOCKET_BUFSIZE = 4096
    # Making a TCP server involves a four-step process of making calls to the
    # create(), bind(), listen() and accept() functions.
    # socket.create_server wraps create() and bind() into a single call
    # and also sets the socket listening mode
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client

    data = None
    while True:
        data = conn.recv(SOCKET_BUFSIZE)
        if data == b'':
            break
        conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
    conn.close()



if __name__ == "__main__":
    main()
