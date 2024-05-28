from flask import Flask, request
import boto3

app = Flask(__name__)

# Configurar el cliente SQS
sqs_client = boto3.client('sqs', region_name='us-east-1')  # Especifica tu región
queue_url = 'https://sqs.us-east-1.amazonaws.com/533267246902/EC2-to-Lambda'

@app.route('/send_message', methods=['POST'])
def send_message():
    # Obtener datos de la solicitud HTTP
    bucket_name = request.form.get('bucket_name')
    root_file = request.form.get('root_file')
    num_files = request.form.get('num_files')

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
    print(f'Message ID: {response["MessageId"]}')
    print(f'MD5 of Message Body: {response["MD5OfMessageBody"]}')

    return 'Mensaje enviado correctamente a la cola SQS'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
