import socket


status_msg = {
    200: "OK",
    404: "Not Found"
}

def build_http_response(status_code: int, text: str):
    response = (
        f"HTTP/1.1 {status_code} {status_msg[status_code]}\r\n\r\n"
        f"Content-type: text/plain\r\n\r\n"
        f"Content-Length: {len(text)}\r\n\r\n"
        f"\r\n\r\n"
        f"{text}"
    )

    return response




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


        response = build_http_response(200, path.split("/")[-1])
        print(f"{response=}")

        conn.send(response.encode())



if __name__ == "__main__":
    main()

