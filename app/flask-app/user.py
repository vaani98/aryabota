import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    email = db.EmailField(primary_key = True)
    age = db.IntField()
    python_programming_experience = db.StringField()
    def to_json(self):
        return {"email": self.email,
                "age": self.age,
                "python_programming_experience": self.python_programming_experience}

@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    '''record = {"email": "abc@gmail.com",
              "age": 18,
              "python_programming_experience": "basic"}'''
    user = User(email = record['email'],
                age = record['age'],
                python_programming_experience = record['python_programming_experience'])
    user.save()
    print(jsonify(user.to_json()))
    #return True
    

@app.route('/', methods=['GET'])
def exists():
    input_email = request.args.get('email')
    user = User.objects(email = input_email).first()
    if not user:
        return False
    else:
        return True
