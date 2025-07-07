import socket

class Cliente:
    def __init__(self, ip='127.0.0.1', puerto=9001):  # Cambié el puerto a 9001
        self.ip = ip
        self.puerto = puerto
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def enviar_mensaje(self):
        self.cliente.connect((self.ip, self.puerto))
        mensaje = input("Escribe un mensaje para el servidor (puede ser texto o número): ")
        self.cliente.send(mensaje.encode())
        print("Mensaje enviado con éxito")  # Mensaje de confirmación agregado (actividad extra)
        self.cliente.close()

if __name__ == "__main__":
    cliente = Cliente()
    cliente.enviar_mensaje()

# Comentarios:
# - Cambié el puerto a 9001 para coincidir con el servidor.
# - Corregí el método constructor de __init__ y el condicional principal.
# - Añadí un mensaje de confirmación cuando el mensaje es enviado correctamente.
# - El input permite enviar texto o números; ambos serán procesados como cadenas.