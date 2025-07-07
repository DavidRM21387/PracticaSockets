import socket

class ServidorChat:
    def __init__(self, ip='127.0.0.1', puerto=8090):
        self.ip = ip
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def iniciar_chat(self):
        self.servidor.bind((self.ip, self.puerto))
        self.servidor.listen(1)
        print(f"Servidor escuchando en {self.ip}:{self.puerto}")
        conexion, direccion = self.servidor.accept()
        print("Conexión establecida con:", direccion)

        while True:
            datos = conexion.recv(1024).decode()
            if datos.lower() == "salir":
                print("El cliente ha cerrado la conexión.")
                break
            print("Cliente:", datos)
            mensaje = input("Servidor: ")
            conexion.send(mensaje.encode())
            if mensaje.lower() == "salir":
                print("Servidor cerró la conexión.")
                break
        conexion.close()

if __name__ == "__main__":
    servidor = ServidorChat()
    servidor.iniciar_chat()