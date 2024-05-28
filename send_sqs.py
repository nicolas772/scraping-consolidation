import logging
from flask import Flask, request
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)  # Habilita CORS en todas las rutas

# Configurar el logging
logging.basicConfig(level=logging.INFO)

@app.before_request
def log_request_info():
    logging.info(f'Received request: {request.method} {request.path}')
    logging.info(f'Headers: {request.headers}')
    logging.info(f'Body: {request.get_data()}')

# Configurar el cliente SQS
sqs_client = boto3.client('sqs', region_name='us-east-1')  # Especifica tu región
queue_url = 'https://sqs.us-east-1.amazonaws.com/533267246902/EC2-to-Lambda'

@app.route('/send_message', methods=['POST'])
def send_message():
    # Obtener datos de la solicitud HTTP
    bucket_name = request.json.get('bucket_name')
    root_file = request.json.get('root_file')
    num_files = request.json.get('num_files')

    # Mensaje que deseas enviar
    message_body = 'New Excel File'

    # Atributos del mensaje
    message_attributes = {
        'bucket-name': {
            'StringValue': bucket_name,
            'DataType': 'String'
        },
        'root-file': {
            'StringValue': root_file,
            'DataType': 'String'
        },
        'num-files': {
            'StringValue': num_files,
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
    logging.info(f'Message ID: {response["MessageId"]}')
    logging.info(f'MD5 of Message Body: {response["MD5OfMessageBody"]}')

    return {'message': 'Mensaje enviado correctamente a la cola SQS'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Habilitar modo debug
