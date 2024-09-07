import paho.mqtt.client as mqtt
import json
import random
import time
import argparse

# Configura el cliente MQTT
broker = "localhost"  # Cambia a la dirección de tu broker
port = 1883  # Puerto del servidor mosquitto

# Inicializa el cliente
client = mqtt.Client()

# Manejo de argumentos
def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulador de dispositivos MQTT.")
    parser.add_argument('-b', '--broker', type=str, default=broker, help='Dirección del broker MQTT (default: localhost).')
    parser.add_argument('-p', '--port', type=int, default=port, help='Puerto del broker MQTT (default: 1883).')
    return parser.parse_args()

try:
    client.connect(broker, port)
    print(f"Conectado al broker {broker} en el puerto {port}")
except Exception as e:
    print(f"Error al conectar al broker: {e}")
    exit(1)  # Salir si no se puede conectar

# Lista de dispositivos simulados
dispositivos = [
    {"id": "dispositivo_1", "variables": ["1", "2"]},
    {"id": "dispositivo_2", "variables": ["1", "3"]},
    {"id": "dispositivo_3", "variables": ["2", "3"]},
]


def publish_data():
    while True:
        for dispositivo in dispositivos:
            for variable_id in dispositivo["variables"]:
                # Generar un valor aleatorio
                valor = random.uniform(0, 100)  # Cambia el rango según tus necesidades

                # Crear el mensaje
                mensaje = {
                    "dispositivo_id": dispositivo["id"],
                    "variable_id": variable_id,
                    "valor": valor
                }

                # Construir el tema específico para cada dispositivo
                topic = f"dispositivo/{dispositivo['id']}/data"

                # Publicar el mensaje en el tema
                client.publish(topic, json.dumps(mensaje))
                print(f"Publicado en {topic}: {mensaje}")

                # Esperar un segundo entre publicaciones
                time.sleep(1)  # Cambia si deseas una frecuencia diferente

            # Esperar un tiempo antes de pasar al siguiente dispositivo
            time.sleep(5)  # Cambia el intervalo según sea necesario


if __name__ == "__main__":
    publish_data()
