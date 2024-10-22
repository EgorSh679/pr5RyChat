import socket
from _thread import *
import threading

# Список для хранения текущих подключений клиентов
clients = []

# Лок для управления доступом к общему списку
lock = threading.Lock()

# Функция для обработки сообщений от клиента
def client_thread(conn, addr):
    conn.send("Добро пожаловать в чат! Напишите что-нибудь.\n".encode())
    
    while True:
        data = conn.recv(1024)
        if not data:
            break

        message = data.decode()
        print(f"{addr} говорит: {message}")
        
        reply = f"Сообщение от {addr}: {message}"

        # Отправка сообщения всем подключенным клиентам
        with lock:
            for client in clients:
                if client != conn:  # Если это не отправитель
                    client.send(reply.encode())

    with lock:
        clients.remove(conn)
    conn.close()

# Настройка сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
port = 12345
server.bind((hostname, port))
server.listen(5)
print("Сервер запущен и ждёт подключения клиентов...")

# Ожидание клиентов
while True:
    client, addr = server.accept()
    with lock:
        clients.append(client)
    print(f"Новое подключение: {addr}")
    start_new_thread(client_thread, (client, addr))
    
server.close()
