import boto3 # type: ignore

# Configura el cliente SQS
sqs_client = boto3.client('sqs', region_name='us-east-1')  # Especifica tu región

# URL de la cola SQS
queue_url = 'https://sqs.us-east-1.amazonaws.com/533267246902/EC2-to-Lambda'

# Mensaje que deseas enviar
message_body = 'Este es el cuerpo de tu mensaje'

# Opcional: puedes añadir atributos al mensaje
message_attributes = {
    'Attribute1': {
        'StringValue': 'Valor de atributo 1',
        'DataType': 'String'
    },
    'Attribute2': {
        'StringValue': 'Valor de atributo 2',
        'DataType': 'String'
    }
}

# Enviar el mensaje
response = sqs_client.send_message(
    QueueUrl=queue_url,
    MessageBody=message_body,
    MessageAttributes=message_attributes
)

# Imprimir el ID del mensaje y el MD5 del cuerpo del mensaje
print(f'Message ID: {response["MessageId"]}')
print(f'MD5 of Message Body: {response["MD5OfMessageBody"]}')
