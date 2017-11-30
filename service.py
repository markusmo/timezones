from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

#database access
todos = {}

class TodoSimple(Resource):
    """
    calculate timezone of coordinate
    a point is always in an area, here it is a timezone-polygon
    """
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
