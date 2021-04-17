import decimal
import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask('__flask__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://calidad:Okinawa.00?@localhost:9000/calidadaireDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Particles API 's
class Particles(db.Model):
    __tablename__ = 'PARTICLES'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)

    def __init__(self, name):
        self.name = name


db.create_all()


class ParticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


particle_schema = ParticleSchema()
particles_schema = ParticleSchema(many=True)


@app.route('/calidadaire/particles', methods=['POST'])
def create_particle():
    name = request.json['name']
    new_particle = Particles(name)
    db.session.add(new_particle)
    db.session.commit()

    return particle_schema.jsonify(new_particle)


@app.route('/calidadaire/particles', methods=['GET'])
def get_particles():
    all_particles = Particles.query.all()
    result = particles_schema.dump(all_particles)
    return jsonify(result)


@app.route('/calidadaire/particle/<id>', methods=['GET'])
def get_particle(id):
    particle = Particles.query.get(id)
    return particle_schema.jsonify(particle)


@app.route('/calidadaire/particle/<id>', methods=['PUT'])
def update_particle(id):
    particle = Particles.query.get(id)

    name = request.json['name']

    particle.name = name

    db.session.commit()
    return particle_schema.jsonify(particle)


@app.route('/calidadaire/particle/<id>', methods=['DELETE'])
def delete_particle(id):
    particle = Particles.query.get(id)

    db.session.delete(particle)
    db.session.commit()

    return particle_schema.jsonify(particle)


# Devices API 's
class Devices(db.Model):
    __tablename__ = 'DEVICES'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    geo = db.Column(db.String(30), nullable=False)
    altitude = db.Column(db.Numeric)

    def __init__(self, name, geo, altitude):
        self.name = name
        self.geo = geo
        self.altitude = altitude


db.create_all()


class DeviceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'geo', 'altitude')


device_schema = DeviceSchema()
dives_schema = DeviceSchema(many=True)


@app.route('/calidadaire/device', methods=['POST'])
def create_device():
    name = request.json['name']
    geo = request.json['geo']
    altitude = request.json['altitude']
    new_device = Devices(name, geo, altitude)
    db.session.add(new_device)
    db.session.commit()

    return device_schema.jsonify(new_device)


@app.route('/calidadaire/devices', methods=['GET'])
def get_devices():
    all_devices = Devices.query.all()
    result = device_schema.dump(all_devices)
    return jsonify(result)


@app.route('/calidadaire/device/<id>', methods=['GET'])
def get_device(id):
    particle = Devices.query.get(id)
    return device_schema.jsonify(particle)


@app.route('/calidadaire/device/<id>', methods=['PUT'])
def update_device(id):
    device = Devices.query.get(id)

    name = request.json['name']
    geo = request.json['geo']
    altitude = request.json['altitude']

    device.name = name
    device.geo = geo
    device.altitude = altitude

    db.session.commit()
    return device_schema.jsonify(device)


@app.route('/calidadaire/device/<id>', methods=['DELETE'])
def delete_device(id):
    device = Devices.query.get(id)

    db.session.delete(device)
    db.session.commit()

    return device_schema.jsonify(device)


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)


if __name__ == '__main__':
    app.run()
