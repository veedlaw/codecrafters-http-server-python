import sys
import socket
import threading
from pathlib import Path
from enum import Enum
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--directory", type=Path, dest="directory")
args = parser.parse_args()

class ContentType(Enum):
    PLAINTEXT = "text/plain"
    OCTET = "application/octet-stream"


status_msg = {
    200: "OK",
    404: "Not Found"
}


def build_http_response(status_code: int, content_type: ContentType, text: str) -> str:
    content_length = len(text)
    response = (
        f"HTTP/1.1 {status_code} {status_msg[status_code]}\r\n"
        f"Content-Type: {content_type.value}\r\n"
        f"Content-Length: {content_length}\r\n"
        f"\n"
        f"{text}\r\n\r\n"
    )

    return response


def parse_user_agent(user_agent_line) -> str:
    _request_header, user_agent = user_agent_line.split(" ")
    return user_agent


def parse_filename(request_target) -> Path:
    filename = request_target[len("/files/"):]
    return Path(filename)


def handle_request(client_conn, address, SOCKET_BUFSIZE = 4096):

    with client_conn:
        data = client_conn.recv(SOCKET_BUFSIZE)

        http_msg_contents = data.decode().split("\r\n")
        msg_start_line = http_msg_contents[0]

        http_method, request_target, http_version = msg_start_line.split(" ")
        http_response = "HTTP/1.1 404 Not Found\r\n\r\n"  # Default value

        if request_target == "/":
            http_response = "HTTP/1.1 200 OK\r\n\r\n"
        elif request_target.startswith("/echo/"):
            http_response = build_http_response(200,
                                                ContentType.PLAINTEXT,
                                                request_target[len("/echo/"):])
        elif request_target == "/user-agent":
            for line in http_msg_contents:
                if line.startswith("User-Agent"):
                    user_agent = parse_user_agent(line)
                    http_response = build_http_response(200, ContentType.PLAINTEXT, user_agent)
                    break
        elif request_target.startswith("/files/"):
            filepath = parse_filename(request_target)
            fullpath = args.directory / filepath
            if fullpath.exists():
                data = fullpath.read_text()
                http_response = build_http_response(200, ContentType.OCTET, data)


        client_conn.send(http_response.encode())




def main():

    HOST = "localhost"
    PORT = 4221

    # Making a TCP server involves a four-step process of making calls to the
    # create(), bind(), listen() and accept() functions.
    # socket.create_server wraps create() and bind() into a single call
    # and also sets the socket listening mode
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)

    while True:
        conn, address = server_socket.accept()
        thread = threading.Thread(target=handle_request, args=(conn, address))
        thread.start()




if __name__ == "__main__":
    main()

