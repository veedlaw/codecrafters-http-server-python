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

    conn, addr = server_socket.accept()
    with conn:
        data = conn.recv(SOCKET_BUFSIZE)
        print(f"{data=}")

        http_msg_contents = data.decode().split("\r\n")
        msg_start_line = http_msg_contents[0]
        request_type, path, protocol = msg_start_line.split(" ")
        if path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")



if __name__ == "__main__":
    main()

