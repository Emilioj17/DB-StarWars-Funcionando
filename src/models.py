from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Persona(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    altura = db.Column(db.String(100), nullable=False)
    masa = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "masa": self.masa,
            "descripcion": self.descripcion
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Planeta(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    diametro = db.Column(db.String(100), nullable=False)
    poblacion = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "poblacion": self.poblacion,
            "descripcion": self.descripcion
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    clave = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "correo": self.correo,
            "clave": self.clave
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Personaje_favorito(db.Model):
    __tablename__ = 'personajes_favoritos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        "usuarios.id"), nullable=False)
    personaje_id = db.Column(db.Integer, db.ForeignKey(
        "personas.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personaje_id": self.personaje_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Planeta_favorito(db.Model):
    __tablename__ = 'planetas_favoritos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        "usuarios.id"), nullable=False)
    planeta_id = db.Column(db.Integer, db.ForeignKey(
        "planetas.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planeta_id": self.planeta_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
