import socket

class Servidor:
    def __init__(self, ip='127.0.0.1', puerto=9001):  # Cambié el puerto a 9001 (actividad extra)
        self.ip = ip
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def iniciar(self):
        self.servidor.bind((self.ip, self.puerto))
        self.servidor.listen(5)
        print(f"Servidor escuchando en {self.ip}:{self.puerto}")
        conexion, direccion = self.servidor.accept()
        print("Conexión establecida con:", direccion)
        datos = conexion.recv(1024)
        print("Mensaje recibido:", datos.decode())
        conexion.close()

if __name__ == "__main__":
    servidor = Servidor()
    servidor.iniciar()

# Comentarios:
# - Cambié el puerto de 8090 a 9001 para reforzar la comprensión sobre la configuración de puertos.
# - Corregí el método constructor de __init__ (tenía init) y el condicional de ejecución principal (tenía name == "main").
# - El código está listo para recibir tanto texto como números, ya que siempre se recibe como string con .decode().