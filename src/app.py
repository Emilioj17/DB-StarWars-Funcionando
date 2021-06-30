import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_migrate import Migrate
from models import db, Contact

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/api/contacts', methods=['GET'])
def list_contact():
    contacts = Contact.query.all()
    contacts = list(map(lambda contact: contact.serialize(), contacts))
    return jsonify(contacts), 200


@app.route('/api/contacts', methods=['POST'])
def create_contact():
    request_body = request.data
    decoded_object = json.loads(request_body)
    name = decoded_object["name"]
    phone = decoded_object["phone"]
    email = decoded_object["email"]
    contact = Contact()
    contact.name = name
    contact.phone = phone
    contact.email = email

    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.serialize())


@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    request_body = request.data
    decoded_object = json.loads(request_body)
    name = decoded_object["name"]
    phone = decoded_object["phone"]
    email = decoded_object["email"]

    contact = Contact.query.get(id)
    contact.name = name
    contact.phone = phone
    contact.email = email

    db.session.commit()

    return jsonify(contact.serialize()), 200


@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):

    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"success": "Contact deleted"}), 200


if __name__ == '__main__':
    app.run()

# @app.route('/todos', methods=['GET'])
# def hello_world():
#     return jsonify(todos)

# todos = [
#     {"label": "My first task", "done": False},
#     {"label": "My second task", "done": False}
# ]

# @app.route('/todos', methods=['POST'])
# def add_new_todo():
#     request_body = request.data
#     decoded_object = json.loads(request_body)
#     # print("Incoming request with the following body", request_body)
#     todos.append(decoded_object)
#     return jsonify(todos)


# @app.route('/todos/<int:position>', methods=['DELETE'])
# def delete_todo(position):
#     todos.pop(position)
#     # print("This is the position to delete: ", position)
#     return jsonify(todos)


# # These two lines should always be at the end of your app.py file.
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3245, debug=True)
