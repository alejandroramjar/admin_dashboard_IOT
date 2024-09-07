import paho.mqtt.client as mqtt
import json


# Almacenar las suscripciones activas
active_subscriptions = {}


def on_message(client, userdata, message):
    from .models import RegistroVariable, Dispositivo, Variable  # Importar aquí para evitar la circularidad
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)

    dispositivo_id = data.get('dispositivo_id')
    variable_id = data.get('variable_id')
    valor = data.get('valor')

    try:
        dispositivo = Dispositivo.objects.get(identificador=dispositivo_id)
        variable = Variable.objects.get(id=variable_id)

        registro = RegistroVariable(dispositivo=dispositivo, variable=variable, valor=valor)
        registro.save()
        print(f'Registro guardado: {registro}')
    except (Dispositivo.DoesNotExist, Variable.DoesNotExist) as e:
        print(f'Error al guardar registro: {e}')


def subscribe_to_device(client, dispositivo_id):
    # Usar un tema único para cada dispositivo
    topic = f"dispositivo/{dispositivo_id}/data"
    client.subscribe(topic)
    print(f'Suscrito al tema: {topic}')
    active_subscriptions[dispositivo_id] = topic


def start_mqtt_client():
    from .models import Dispositivo
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()

    # Suscribirse a los dispositivos existentes al iniciar
    for dispositivo in Dispositivo.objects.all():
        subscribe_to_device(client, dispositivo.identificador)