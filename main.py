from typing import Union

from fastapi import FastAPI # type: ignore
from pydantic import BaseModel
import boto3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el cliente SQS
sqs_client = boto3.client('sqs', region_name='us-east-1')  # Especifica tu región
queue_url = 'https://sqs.us-east-1.amazonaws.com/533267246902/EC2-to-Lambda'


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.put("/send-message")
def send_message():
    """
    bucket_name = request.json.get('bucket_name')
    root_file = request.json.get('root_file')
    num_files = request.json.get('num_files')
    """
    bucket_name = 'bank-consolidation-2'
    root_file = 'cartola_parte_'
    num_files = '1' 

    # Mensaje que deseas enviar
    message_body = 'New Excel File from EC2'

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
    return {'message': 'Mensaje enviado correctamente a la cola SQS'}