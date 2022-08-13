from shutil import register_unpack_format
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields
from flask_restful import marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

class todo_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(100))
    Rank = db.Column(db.String(100))

# db.create_all()

# taking arguments
take_post_args = reqparse.RequestParser()
take_post_args.add_argument("language", type=str, help="this is required field", required=True)
take_post_args.add_argument("Rank", type=int, help="this is required field", required=True)

take_update_args = reqparse.RequestParser()
take_update_args.add_argument("language", type=str)
take_update_args.add_argument("Rank", type=int)

resource_fields = {
    'id' : fields.Integer,
    'language' : fields.String,
    'Rank' : fields.String,
}


class todolist_show(Resource):
    def get(self):
        task = todo_model.query.all()
        todo_list = {}
        for i in task:
            todo_list[i.id] = {"language":i.language, "Rank":i.Rank}
        return todo_list


class todo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = todo_model.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="couldn't find a task with that id")
        return task

    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = take_post_args.parse_args()
        task = todo_model.query.filter_by(id=todo_id).first()
        if task:
            abort(409, message="ID already taken")
        td = todo_model(id=todo_id, language=args['language'], Rank=args['Rank'])
        db.session.add(td)
        db.session.commit()
        return td, 201

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = take_update_args.parse_args()
        task = todo_model.query.filter_by(id=todo_id).first()

        if not task:
            abort(404, message="not found!!, unable to update")
        if args['language']:
            task.language = args['language']
        if args['Rank']:
            task.Rank = args['Rank']
        db.session.commit()
        return task

    def delete(self, todo_id):
        task = todo_model.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        return 'deleted',204

#adding to the API
api.add_resource(todo, '/todo_list/<int:todo_id>')
api.add_resource(todolist_show, '/todo_list/')

if __name__ == "__main__":
    app.run(debug=True)

