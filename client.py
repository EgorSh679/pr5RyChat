import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Сервер: {message}")
            else:
                break
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
port = 12345

try:
    client.connect((hostname, port))
except:
    print("Ошибка подключения!")

# Запуск отдельного потока для получения сообщений
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

while True:
    user_input = input()
    if user_input.lower() == 'exit':
        break
    client.send(user_input.encode())

client.close()
