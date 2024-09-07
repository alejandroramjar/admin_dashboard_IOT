import paho.mqtt.client as mqtt
import json
import random
import time
import argparse

# Configura el cliente MQTT
broker = "localhost"  # Cambia a la dirección de tu broker
port = 1883  # Puerto del servidor Mosquitto

# Inicializa el cliente
client = mqtt.Client()


# Manejo de argumentos
def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulador de dispositivos MQTT.")
    parser.add_argument('-b', '--broker', type=str, default=broker,
                        help='Dirección del broker MQTT (default: localhost).')
    parser.add_argument('-p', '--port', type=int, default=port, help='Puerto del broker MQTT (default: 1883).')
    return parser.parse_args()


try:
    args = parse_arguments()
    client.connect(args.broker, args.port)
    print(f"Conectado al broker {args.broker} en el puerto {args.port}")
except Exception as e:
    print(f"Error al conectar al broker: {e}")
    exit(1)  # Salir si no se puede conectar

# Lista de dispositivos simulados y sus variables
dispositivos = [
    {"id": "dispositivo_1", "variables": [
        {"id": "temperatura", "nombre": "Temperatura"},
        {"id": "humedad", "nombre": "Humedad Relativa"}
    ]},
    {"id": "dispositivo_2", "variables": [
        {"id": "presion", "nombre": "Presión Atmosférica"},
        {"id": "velocidad_viento", "nombre": "Velocidad del Viento"}
    ]},
    {"id": "dispositivo_3", "variables": [
        {"id": "precipitacion", "nombre": "Precipitación"},
        {"id": "radiacion_solar", "nombre": "Radiación Solar"},
        {"id": "temperatura", "nombre": "Temperatura"}
    ]},
    {"id": "dispositivo_4", "variables": [
        {"id": "temperatura_suelo", "nombre": "Temperatura del Suelo"},
        {"id": "humedad", "nombre": "Humedad Relativa"}
    ]},
]


def publish_data():
    while True:
        for dispositivo in dispositivos:
            for variable in dispositivo["variables"]:
                # Generar un valor aleatorio
                if variable["id"] == "temperatura":
                    valor = random.uniform(15.0, 35.0)  # Rango de temperatura
                elif variable["id"] == "humedad":
                    valor = random.uniform(30.0, 90.0)  # Rango de humedad
                elif variable["id"] == "presion":
                    valor = random.uniform(950.0, 1050.0)  # Rango de presión
                elif variable["id"] == "velocidad_viento":
                    valor = random.uniform(0.0, 15.0)  # Rango de velocidad del viento
                elif variable["id"] == "precipitacion":
                    valor = random.uniform(0.0, 100.0)  # Rango de precipitación
                elif variable["id"] == "radiacion_solar":
                    valor = random.uniform(0.0, 1000.0)  # Rango de radiación solar
                elif variable["id"] == "temperatura_suelo":
                    valor = random.uniform(10.0, 30.0)  # Rango de temperatura del suelo

                # Crear el mensaje
                mensaje = {
                    "dispositivo_id": dispositivo["id"],
                    "variable_id": variable["id"],
                    "variable_nombre": variable["nombre"],
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
