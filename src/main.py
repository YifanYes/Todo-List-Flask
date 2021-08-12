import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Account, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# Metodos Get

@app.route('/user', methods=['GET'])
def get_user():
    all_user = Account.get_all() 
    if all_user:
        return jsonify(all_user), 200

    return jsonify({'message': 'No account created'}), 500

#Todos los task 
@app.route('/user/<int:id>/tasks', methods=['GET'])
def get_task(id):

    user_tasks = Task.get_task_by_user(id) 

    if not user_tasks:
        return jsonify({'message': 'No tasks yet'}), 200

    return jsonify(user_tasks), 200
    
#Task specific
@app.route('/user/<int:id>/tasks/<int:position>', methods=['GET'])
def get_specific_task(id, position):

    user_tasks = Task.get_task_by_user(id) 

    #add filtrado por status active y por position.


    if not user_tasks:
        return jsonify({'message': 'Not specific task found'}), 200

    return jsonify(user_tasks), 200

#Metodos post

@app.route('/user', methods=['POST'])
def create_user_task():

    nick = request.json.get('nick', None)
    
    if not (nick):
        return {'error': 'Missing info'}, 400

    user= Account(nick = nick)
    user.create()

    return jsonify(user.to_dict()),201

    
@app.route('/user/<int:id>/tasks', methods=['POST'])
def add_new_task(id):
    label = request.json.get('label', None)
    status = request.json.get('status', None)
    
    if not (label and status and id):
        return {'error': 'No enough info'}, 400

    task= Task(label = label, status=status, account_id=id)
    task.add_new()

    return jsonify(task.to_dict()),201

    print("Incoming request", request_body)
    return jsonify(task)

#Metodo delete

@app.route('/user', methods=['POST'])
def delete_user_task():

    task_delete = request.json.get('nick', None)
    
    if not (nick):
        return {'error': 'Missing info'}, 400

    user= Account(nick = nick)
    user.create()

    return jsonify(user.to_dict()),201



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)