import json
from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate
from models import db, Persona, Planeta, Usuario, Personaje_favorito, Planeta_favorito

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)


# Main html
@app.route('/')
def main():
    return render_template('index.html')


# Primera Parte de Tarea  People, People int, Planets, Planets int
@app.route('/api/personas', methods=['GET'])
def list_personas():
    personas = Persona.query.all()
    personas = list(map(lambda persona: persona.serialize(), personas))
    return jsonify(personas), 200


@app.route('/api/personas/<int:id>', methods=['GET'])
def info_persona(id):
    persona = Persona.query.get(id)
    return jsonify(persona.serialize()), 200


@app.route('/api/planetas', methods=['GET'])
def list_planetas():
    planetas = Planeta.query.all()
    planetas = list(map(lambda planeta: planeta.serialize(), planetas))
    return jsonify(planetas), 200


@app.route('/api/planetas/<int:id>', methods=['GET'])
def info_planeta(id):
    planeta = Planeta.query.get(id)
    return jsonify(planeta.serialize()), 200


# Segunda Parte de Tarea: Usuarios, usuarios Favoritos
# Get, Post y Delete
@app.route('/api/usuarios', methods=['GET'])
def list_usuarios():
    usuarios = Usuario.query.all()
    usuarios = list(map(lambda usuario: usuario.serialize(), usuarios))
    return jsonify(usuarios), 200


# Retorna Planetas y Personajes Favoritos segun Usuario
@app.route('/api/usuarios/<int:id>', methods=['GET'])
def list__favortios_usuarios(id):
    personajes_favoritos_usuario = Personaje_favorito.query.filter_by(
        usuario_id=id)
    planetas_favoritos_usuario = Planeta_favorito.query.filter_by(
        usuario_id=id)

    personajes_favoritos_usuario = list(
        map(lambda favorito: favorito.serialize(), personajes_favoritos_usuario))
    planetas_favoritos_usuario = list(
        map(lambda favorito: favorito.serialize(), planetas_favoritos_usuario))
    return jsonify(personajes_favoritos_usuario + planetas_favoritos_usuario), 200


# Post a Personaje Favorito según id Usuario
@app.route('/api/usuarios/personaje/<int:id>', methods=['POST'])
def create_personaje(id):
    request_body = request.data
    decoded_object = json.loads(request_body)
    usuario_id = id
    personaje_id = decoded_object["personaje_id"]

    personaje = Personaje_favorito()
    personaje.usuario_id = usuario_id
    personaje.personaje_id = personaje_id

    db.session.add(personaje)
    db.session.commit()

    return jsonify(personaje.serialize())


# Post a Planeta Favorito según id Usuario
@app.route('/api/usuarios/planeta/<int:id>', methods=['POST'])
def create_planeta_favorito(id):
    request_body = request.data
    decoded_object = json.loads(request_body)
    usuario_id = id
    planeta_id = decoded_object["planeta_id"]
    planeta = Planeta_favorito()
    planeta.usuario_id = usuario_id
    planeta.planeta_id = planeta_id

    db.session.add(planeta)
    db.session.commit()

    return jsonify(planeta.serialize())


# Delete
@app.route('/api/usuarios/personaje/<int:id>', methods=['DELETE'])
def delete_personaje(id):

    personajes_favoritos_usuario = Personaje_favorito.query.filter(
        Personaje_favorito.usuario_id == id).first()
    db.session.delete(personajes_favoritos_usuario)
    db.session.commit()

    return jsonify({"success": "Personaje Favorito deleted"}), 200


@app.route('/api/usuarios/planeta/<int:id>', methods=['DELETE'])
def delete_planeta(id):
    planetas_favoritos_usuario = Planeta_favorito.query.filter(
        Planeta_favorito.usuario_id == id)
    db.session.delete(planetas_favoritos_usuario)
    db.session.commit()

    return jsonify({"success": "Planeta Favorito deleted"}), 200


# Solo para Ingresar Personas/Planetas a BD y Usuarios
@app.route('/api/personas', methods=['POST'])
def create_persona():
    request_body = request.data
    decoded_object = json.loads(request_body)
    nombre = decoded_object["nombre"]
    altura = decoded_object["altura"]
    masa = decoded_object["masa"]
    descripcion = decoded_object["descripcion"]
    persona = Persona()
    persona.nombre = nombre
    persona.altura = altura
    persona.masa = masa
    persona.descripcion = descripcion

    db.session.add(persona)
    db.session.commit()

    return jsonify(persona.serialize())


@app.route('/api/planetas', methods=['POST'])
def create_planeta():
    request_body = request.data
    decoded_object = json.loads(request_body)
    nombre = decoded_object["nombre"]
    diametro = decoded_object["diametro"]
    poblacion = decoded_object["poblacion"]
    descripcion = decoded_object["descripcion"]
    planeta = Planeta()
    planeta.nombre = nombre
    planeta.diametro = diametro
    planeta.poblacion = poblacion
    planeta.descripcion = descripcion

    db.session.add(planeta)
    db.session.commit()

    return jsonify(planeta.serialize())


@app.route('/api/usuarios', methods=['POST'])
def create_usuario():
    request_body = request.data
    decoded_object = json.loads(request_body)
    correo = decoded_object["correo"]
    clave = decoded_object["clave"]
    usuario = Usuario()
    usuario.correo = correo
    usuario.clave = clave

    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario.serialize())

# @app.route('/api/people/<int:id>', methods=['PUT'])
# def update_persona(id):
#     request_body = request.data
#     decoded_object = json.loads(request_body)
#     name = decoded_object["name"]
#     phone = decoded_object["phone"]
#     email = decoded_object["email"]

#     persona = Persona.query.get(id)
#     persona.name = name
#     persona.phone = phone
#     persona.email = email

#     db.session.commit()

#     return jsonify(persona.serialize()), 200


# @app.route('/api/people/<int:id>', methods=['DELETE'])
# def delete_persona(id):

#     persona = Persona.query.get(id)
#     db.session.delete(persona)
#     db.session.commit()

#     return jsonify({"success": "persona deleted"}), 200


if __name__ == '__main__':
    app.run()
