import socket
import threading

string_list = []


def handle_client(client_socket):
    global string_list
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Recebido: {request}")

    if request == "GET_LIST":
        response = "\n".join(string_list).encode('utf-8')
        client_socket.send(response)
    else:
        string_list.append(request)
        response = "String recebida com sucesso.".encode('utf-8')
        client_socket.send(response)

    client_socket.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, 8888))
    server.listen(5)
    print("Servidor escutando na porta 8888 IP: " + IP)

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão recebida de {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
