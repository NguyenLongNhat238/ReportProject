import pika
import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from property.models import Property
params = pika.URLParameters('amqp://report:report@172.16.0.174:5672')

connection = pika.BlockingConnection(params)


channel = connection.channel()

channel.queue_declare(queue='report')


def callback(ch, method, properties, body):
    print('received in admin')
    print('im report')
    data = json.loads(body)
    print(data)
    if properties.content_type == 'property_created':
        try:
            Property.objects.using('default').create(
                title=data['title'], price=data['price'], surface=data['surface'], full_address=data['full_address'])
        except:
            print("can't saved")


channel.basic_consume(
    queue='report', on_message_callback=callback, auto_ack=True)


print('start Consuming')

channel.start_consuming()

channel.close()
