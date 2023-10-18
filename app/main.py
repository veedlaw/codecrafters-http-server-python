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



def parse_user_agent(user_agent_line):
    _request_header, user_agent = user_agent_line.split(" ")
    return user_agent


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

        http_method, request_target, http_version = msg_start_line.split(" ")
        http_response = None

        if request_target == "/":
            http_response = "HTTP/1.1 200 OK\r\n\r\n"
        elif request_target.startswith("/echo/"):
            http_response = build_http_response(200, request_target[len("/echo/"):])
        elif request_target == "/user-agent":
            for line in http_msg_contents:
                if line.startswith("User-Agent"):
                    user_agent = parse_user_agent(line)
                    http_response = build_http_response(200, user_agent)
        else:
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

        conn.send(http_response.encode())



if __name__ == "__main__":
    main()

