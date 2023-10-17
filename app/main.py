import socket


status_msg = {
    200: "OK",
    404: "Not Found"
}

def build_http_response(status_code: int, text: str) -> str:
    content_length = len(text)
    response = (
        f"HTTP/1.1 {status_code} {status_msg[status_code]}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Content-Length: {content_length}\r\n"
        f"\n"
        f"{text}\r\n\r\n"
    )

    return response


def main():

    HOST = "localhost"
    PORT = 4221
    SOCKET_BUFSIZE = 4096

    # Making a TCP server involves a four-step process of making calls to the
    # create(), bind(), listen() and accept() functions.
    # socket.create_server wraps create() and bind() into a single call
    # and also sets the socket listening mode
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)

    conn, _ = server_socket.accept()


    with conn:
        data = conn.recv(SOCKET_BUFSIZE)

        http_msg_contents = data.decode().split("\r\n")
        msg_start_line = http_msg_contents[0]
        request_type, path, protocol = msg_start_line.split(" ")
        if path == "/":
            conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
        elif path.startswith("/echo/"):
            response = build_http_response(200, path[len("/echo/"):])
            conn.send(response.encode())
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")



if __name__ == "__main__":
    main()

