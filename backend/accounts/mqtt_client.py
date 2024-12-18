import paho.mqtt.client as mqtt
import json
from .alerta import enviar_aviso
from datetime import datetime
import time
import threading


# Almacenar las suscripciones activas
active_subscriptions = {}


def on_message(client, userdata, message):
    from .models import RegistroVariable, Dispositivo, Variable
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)

    dispositivo_id = data.get('dispositivo_id')
    variable_nombre = data.get('variable_nombre')
    valor = data.get('valor')

    try:
        dispositivo = Dispositivo.objects.get(nombre_identificador=dispositivo_id)
        variable = Variable.objects.get(nombre=variable_nombre)

        # Verifica si ya existe un registro para evitar duplicados
        if not RegistroVariable.objects.filter(dispositivo=dispositivo, variable=variable, valor=valor, timestamp__date=datetime.today()).exists():
            registro = RegistroVariable(dispositivo=dispositivo, variable=variable, valor=valor)
            registro.save()

            # Verificar límites
            if (variable.limite_superior is not None and valor > variable.limite_superior) or \
                    (variable.limite_inferior is not None and valor < variable.limite_inferior):
                enviar_aviso(variable, valor)

            print(f'Registro guardado: {registro}')
        else:
            print(f'Registro duplicado: {dispositivo} - {variable} - {valor}')

    except (Dispositivo.DoesNotExist, Variable.DoesNotExist) as e:
        print(f'Error al guardar registro: {e}')


def subscribe_to_device(client, dispositivo_id):
    # Usar un tema único para cada dispositivo
    topic = f"dispositivo/{dispositivo_id}/data"
    client.subscribe(topic)
    print(f'Suscrito al tema: {topic}')
    active_subscriptions[dispositivo_id] = topic

def check_for_new_devices(client):
    while True:
        # Verificar y suscribirse a nuevos dispositivos
        from .models import Dispositivo
        dispositivos_existentes = {d.nombre_identificador for d in Dispositivo.objects.all()}

        # Suscribirse a dispositivos que no están actualmente suscritos
        for dispositivo_id in dispositivos_existentes:
            if dispositivo_id not in active_subscriptions:
                subscribe_to_device(client, dispositivo_id)

        # Esperar 5 segundos antes de verificar de nuevo
        time.sleep(5)


def start_mqtt_client():
    from .models import Dispositivo
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()

    # Suscribirse a los dispositivos existentes al iniciar
    for dispositivo in Dispositivo.objects.all():
        subscribe_to_device(client, dispositivo.nombre_identificador)
        
    # Iniciar el hilo para verificar nuevos dispositivos
    threading.Thread(target=check_for_new_devices, args=(client,), daemon=True).start()
