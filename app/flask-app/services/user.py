from flask import Flask, request
from services.mongodb import insert_one, exists

import json

app = Flask(__name__)

@app.route('/create_record', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    input = {"email": record['email'],
            "age": record['age'],
            "python_programming_experience": record['python_programming_experience']}
    insert_one("User",input)
    return True

@app.route('/find_record', methods=['PUT'])
def find_record():
    record = json.loads(request.data)
    input_email = record['email']
    #print(exists(input_email))
    return exists(input_email)