from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

partapp = Flask(__name__)
partapp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://calidad:Okinawa.00?@localhost:9000/calidadaireDB'
partapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dbpart = SQLAlchemy(partapp)
mapart = Marshmallow(partapp)


class Particles(dbpart.Model):
    __tablename__ = 'PARTICLES'

    id = dbpart.Column(dbpart.Integer, primary_key=True, autoincrement=True)
    name = dbpart.Column(dbpart.String(10), nullable=False)

    def __init__(self, name):
        self.name = name


dbpart.create_all()


class ParticleSchema(mapart.Schema):
    class Meta:
        fields = ('id', 'name')


particle_schema = ParticleSchema()
particles_schema = ParticleSchema(many=True)


@partapp.route('/calidadaire/particles', methods=['POST'])
def create_particle():
    name = request.json['name']
    new_particle = Particles(name)
    dbpart.session.add(new_particle)
    dbpart.session.commit()

    return particle_schema.jsonify(new_particle)


@partapp.route('/calidadaire/particles', methods=['GET'])
def get_particles():
    all_particles = Particles.query.all()
    result = particles_schema.dump(all_particles)
    return jsonify(result)


@partapp.route('/calidadaire/particle/<id>', methods=['GET'])
def get_particle(id):
    particle = Particles.query.get(id)
    return particle_schema.jsonify(particle)


@partapp.route('/calidadaire/particle/<id>', methods=['PUT'])
def update_particle(id):
    particle = Particles.query.get(id)

    name = request.json['name']

    particle.name = name

    dbpart.session.commit()
    return particle_schema.jsonify(particle)


@partapp.route('/calidadaire/particle/<id>', methods=['DELETE'])
def delete_particle(id):
    particle = Particles.query.get(id)

    dbpart.session.delete(particle)
    dbpart.session.commit()

    return particle_schema.jsonify(particle)
