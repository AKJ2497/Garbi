import pika

credentials = pika.PlainCredentials('newadmin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.145', 5672, '/', credentials)) 
channel = connection.channel()

channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False) 

channel.queue_declare(queue='sciot.temperature')

channel.queue_bind(queue='sciot.temperature', exchange='sciot.topic', routing_key='u38.0.353.*.temperature.*')


def callback(ch, method, properties, body): 
	print('Received: {}'.format(body))


channel.basic_consume(queue='sciot.temperature', on_message_callback=callback, auto_ack=True) 
print('Waiting for messages')
channel.start_consuming()
