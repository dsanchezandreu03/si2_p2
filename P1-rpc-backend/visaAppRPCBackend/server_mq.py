# Uses rabbitMQ as the server

import os
import sys
import django
import pika

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visaSite.settings')

django.setup()

from visaAppRPCBackend.models import Tarjeta, Pago

def main():
    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()
    
    hostname = sys.argv[1]
    port = sys.argv[2]

    # TODO: completar segun las indicaciones
    # 1º) Crear una conexión con el servidor RabbitMQ
    credentials = pika.PlainCredentials('alumnomq', 'alumnomq')
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=hostname,
                port=port,
                credentials=credentials
            )
        )
        channel = connection.channel()
    except Exception as e:
        print(f"Error al conectar con RabbitMQ: {e}")
        exit()

    # 2º) Crear una cola de mensajes usando el canal de comunicación creado
    channel.queue_declare(queue='pago_cancelacion')

    # 3º) Crear y registrar una función de callback 
    # que procesará los mensajes recibidos en la cola de mensajes
    def callback(ch, method, properties, body):
        id_pago = body.decode()
        print(f"[x] Mensaje recibido. Cancelar pago con id={id_pago}")

        try:
            pago = Pago.objects.get(pk=int(id_pago))
            pago.codigoRespuesta = '111'
            pago.save()
            print(f"[OK] Pago {id_pago} cancelado correctamente")
        except Pago.DoesNotExist:
            print(f"[ERROR] No existe un pago con id={id_pago}")
        except Exception as e:
            print(f"[ERROR] No se pudo cancelar el pago {id_pago}: {e}")
    
    # 4º) Comienzo de consumo de mensajes 
    # y registro de la función de callback para la cola de mensajes creada
    channel.basic_consume(
        queue='pago_cancelacion',
        on_message_callback=callback,
        auto_ack=True
    )
    
    print("[*] Esperando mensajes en la cola 'pago_cancelación'...")
    channel.start_consuming()

if __name__ == "__main__":
    main()