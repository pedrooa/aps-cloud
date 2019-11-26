from flask import Flask
from flask_restful import Api, Resource, reqparse, fields,marshal
import os
import requests

app = Flask(__name__)
api = Api(app)

with open('connector.txt') as f:
    eip = f.readline()
eip = eip.rstrip()


# eipConnector = str(os.environ['eipConnector'])

url = "http://"+eip+":8080/"
print("URL: ",url)
task_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = "", location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        tarefas = requests.get(url+"tarefas")
        return {'tarefas': [marshal(tarefa, task_fields) for tarefa in tarefas]}

    def post(self):
        args = self.reqparse.parse_args()
        r = requests.post(url+"tarefas",data={"title":args['title'],"description":args['description']})
        return {'task': marshal(r, task_fields)}, 201

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,help = 'No task title provided' ,location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        super(TaskAPI, self).__init__()
    def get(self, id):
        tarefa = requests.get(url+"tarefa")
        return {'task': tarefa}

    def put(self, id):
        args = self.reqparse.parse_args()
        tarefa = requests.put(url+"tarefa/"+_id,data = {"id":args['_id'],"title":args['title'],"description":args['description']})
        return {'Updated task': tarefa}

    def delete(self, id):
        r = requests.delete(url+"tarefa/"+_id)
        return {'result': True}

class HealthcheckAPI(Resource):

    def get(self):
        return {},200


api.add_resource(TaskListAPI, '/tarefas', endpoint = 'tarefas')
api.add_resource(TaskAPI, '/tarefa/<int:id>', endpoint = 'tarefa')
api.add_resource(HealthcheckAPI, '/healthcheck', endpoint = 'healthcheck')

if __name__ == '__main__':

    app.run( host = os.getenv('LISTEN','0.0.0.0'),port=int(os.getenv('PORT','8080')),debug=True)



