from flask import Flask
from flask_restful import Api, Resource, reqparse, fields,marshal
import os

app = Flask(__name__)
api = Api(app)


class Tarefas:
    def __init__(self,_id,title, description = ""):
        self._id = _id
        self.title = title
        self.description = description


tasks = {
	0:Tarefas(0,"acordar","conseguir"),
	1:Tarefas(1,"cafe","ou baer mate"),
	2:Tarefas(2,"Cloud","claudio")
}

def dictToJson(objectDict):
    json_dict = {}
    for key in objectDict:
        task = objectDict[key].__dict__
        json_dict[key] = task
    return json_dict

class TaskListAPI(Resource):
    def __init__(self):

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = "", location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {"tarefas":dictToJson(tasks)},200


    def post(self):
        args = self.reqparse.parse_args()
        task = Tarefas(len(tasks)+1,args['title'],args['description'])
        tasks[len(tasks)+1] = task
        return {'task': marshal(task, task_fields)}, 201

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,help = 'No task title provided' ,location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        super(TaskAPI, self).__init__()
    def get(self, id):
        task = [task for task in tasks if tasks[task]._id == id]
        if len(task) == 0:
            abort(404)
        jsonTasks = dictToJson(tasks)
        return {'task': jsonTasks[task[0]]}

    def put(self, id):
        task = [task for task in tasks if tasks[task]._id == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            print("{}, {}\n".format(k,v))
            if v is not None:
                if k =="title":

                    tasks[task].title = v
                if k =="description":

                    tasks[task].description = v
        jsonTasks = dictToJson(tasks)
        return {'Updated task': jsonTasks[task]}

    def delete(self, id):
        task = [task for task in tasks if tasks[task]._id == id]
        if len(task) == 0:
            abort(404)
        del tasks[task[0]]
        return {'result': True}

class HealthcheckAPI(Resource):

    def get(self):
        return {},200


api.add_resource(TaskListAPI, '/tarefas', endpoint = 'tarefas')
api.add_resource(TaskAPI, '/tarefa/<int:id>', endpoint = 'tarefa')
api.add_resource(HealthcheckAPI, '/healthcheck', endpoint = 'healthcheck')

if __name__ == '__main__':

    app.run( host = os.getenv('LISTEN','0.0.0.0'),port=int(os.getenv('PORT','8080')),debug=True)



