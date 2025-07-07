import socket

class Cliente:
    def __init__(self, ip='127.0.0.1', puerto=8090):
        self.ip = ip
        self.puerto = puerto
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def comunicarse(self):
        self.cliente.connect((self.ip, self.puerto))
        mensaje = input("Escribe un mensaje para el servidor: ")
        self.cliente.send(mensaje.encode())
        respuesta = self.cliente.recv(1024).decode()
        print("Respuesta del servidor:", respuesta)
        # Actividad extra 3: Mensaje de despedida
        print("¡Hasta luego! Gracias por comunicarte con el servidor.")
        self.cliente.close()

if __name__ == "__main__":
    cliente = Cliente()
    cliente.comunicarse()