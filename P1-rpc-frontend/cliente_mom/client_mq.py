import pika
import sys

def cancelar_pago(hostname, port, id_pago): 
    credentials = pika.PlainCredentials('alumnomq', 'alumnomq')

    try:
        # TODO: conectar con rabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=hostname,
                port=port,
                credentials=credentials
            )
        )
        channel = connection.channel()

        channel.queue_declare(queue='pago_cancelacion')

        channel.basic_publish(
            exchange='',
            routing_key='pago_cancelacion',
            body=str(id_pago)
        )

        print(f"[x] Solicitud de cancelación enviada para idPago={id_pago}")

        connection.close()

    except Exception as e:
        print("Error al conectar al host remoto")
        exit()

def main():

    if len(sys.argv) != 4:
        print("Debe indicar el host, el numero de puerto, y el ID del pago a cancelar como un argumento.")
        exit()

    cancelar_pago(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()