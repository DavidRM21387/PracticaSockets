import socket

class Servidor:
    def __init__(self, ip='127.0.0.1', puerto=8090):
        self.ip = ip
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def iniciar(self):
        self.servidor.bind((self.ip, self.puerto))
        self.servidor.listen(5)
        print(f"Servidor escuchando en {self.ip}:{self.puerto}")
        conexion, direccion = self.servidor.accept()
        print("Conexión establecida con:", direccion)

        datos = conexion.recv(1024).decode()
        print("Mensaje recibido del cliente:", datos)

        # Actividad extra 1 y 2: Personalización de la respuesta
        nombre = self.obtener_nombre(datos)
        if nombre:
            respuesta = f"¡Gracias {nombre}! Recibí tu mensaje: '{datos}'."
        else:
            respuesta = f"¡Gracias! Recibí tu mensaje: '{datos}'."

        conexion.send(respuesta.encode())
        conexion.close()

    def obtener_nombre(self, mensaje):
        """
        Busca si el mensaje contiene la palabra 'nombre: <nombre>'.
        Por ejemplo: 'Hola, mi nombre: Juan'
        """
        if 'nombre:' in mensaje:
            partes = mensaje.split('nombre:')
            if len(partes) > 1:
                # Toma lo que sigue de 'nombre:' y lo limpia
                nombre = partes[1].split()[0].strip(",.;")
                return nombre
        return None

if __name__ == "__main__":
    servidor = Servidor()
    servidor.iniciar()