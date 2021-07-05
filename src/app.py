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
@app.route('/api/personas', methods=['GET', 'POST'])
@app.route('/api/personas/<int:id>', methods=['GET'])
def list_personas(id=None):
    if (request.method == 'GET'):
        if(id is not None):
            persona = Persona.query.get(id)
            return jsonify(persona.serialize()), 200
        personas = Persona.query.all()
        personas = list(map(lambda persona: persona.serialize(), personas))
        return jsonify(personas), 200

    if (request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        nombre = decoded_object['nombre']
        altura = decoded_object['altura']
        masa = decoded_object['masa']
        descripcion = decoded_object['descripcion']
        persona = Persona()
        persona.nombre = nombre
        persona.altura = altura
        persona.masa = masa
        persona.descripcion = descripcion
        persona.save()

        return jsonify(persona.serialize())


@app.route('/api/planetas', methods=['GET', 'POST'])
@app.route('/api/planetas/<int:id>', methods=['GET'])
def list_planetas(id=None):
    if(request.method == 'GET'):
        if(id is not None):
            planeta = Planeta.query.get(id)
            return jsonify(planeta.serialize()), 200
        planetas = Planeta.query.all()
        planetas = list(map(lambda planeta: planeta.serialize(), planetas))
        return jsonify(planetas), 200

    if(request.method == 'POST'):
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

        planeta.save()

        return jsonify(planeta.serialize())


# Segunda Parte de Tarea: Usuarios, usuarios Favoritos
@app.route('/api/usuarios', methods=['GET', 'POST'])
@app.route('/api/usuarios/<int:id>', methods=['GET'])
def list_usuarios(id=None):
    if(request.method == 'GET'):
        if(id is not None):
            # Retorna Planetas y Personajes Favoritos segun Usuario
            personajes_favoritos_usuario = Personaje_favorito.query.filter_by(
                usuario_id=id)
            planetas_favoritos_usuario = Planeta_favorito.query.filter_by(
                usuario_id=id)
            personajes_favoritos_usuario = list(
                map(lambda favorito: favorito.serialize(), personajes_favoritos_usuario))
            planetas_favoritos_usuario = list(
                map(lambda favorito: favorito.serialize(), planetas_favoritos_usuario))
            return jsonify(personajes_favoritos_usuario + planetas_favoritos_usuario), 200
        usuarios = Usuario.query.all()
        usuarios = list(map(lambda usuario: usuario.serialize(), usuarios))
        return jsonify(usuarios), 200

    if(request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        correo = decoded_object["correo"]
        clave = decoded_object["clave"]
        usuario = Usuario()
        usuario.correo = correo
        usuario.clave = clave
        usuario.save()

        return jsonify(usuario.serialize())


# Post a Personaje Favorito según id Usuario
@app.route('/api/usuarios/personaje/<int:id>', methods=['POST'])
def create_personaje(id):
    if(request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        usuario_id = id
        personaje_id = decoded_object["personaje_id"]

        personaje = Personaje_favorito()
        personaje.usuario_id = usuario_id
        personaje.personaje_id = personaje_id
        personaje.save()

        return jsonify(personaje.serialize())


# Post a Planeta Favorito según id Usuario
@app.route('/api/usuarios/planeta/<int:id>', methods=['POST'])
def create_planeta_favorito(id):
    if(request.method == 'POST'):
        request_body = request.data
        decoded_object = json.loads(request_body)
        usuario_id = id
        planeta_id = decoded_object["planeta_id"]
        planeta = Planeta_favorito()
        planeta.usuario_id = usuario_id
        planeta.planeta_id = planeta_id
        planeta.save()

        return jsonify(planeta.serialize())


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
        Planeta_favorito.usuario_id == id).first()
    db.session.delete(planetas_favoritos_usuario)
    db.session.commit()

    return jsonify({"success": "Planeta Favorito deleted"}), 200


if __name__ == '__main__':
    app.run()
