import datetime

from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask import session
import arrow
from datetime import date
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask('__flask__')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1qaw3edr5tg@192.168.1.102:9000/calidadaireDB'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
PORT = 5000
DEBUG = False
app.secret_key = '5HnNaFgcBVNxkUswJ74eImPJQuXSvecr'

db = SQLAlchemy(app)
ma = Marshmallow(app)

SWAGGER_URL = '/documentation'
app_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    app_URL,
    config={
        'app_name': "Calidad del aire Back-end - UEB"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# User Types
class UserTypes(db.Model):
    __tablename__ = 'USER_TYPES'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name


class UserTypesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


usertype_schema = UserTypesSchema()
usertypes_schema = UserTypesSchema(many=True)


@app.route('/calidadaire/usertypes', methods=['POST'])
def create_usertypes():
    name = request.json['name']
    new_usertype = UserTypes(name)
    db.session.add(new_usertype)
    db.session.commit()
    return usertype_schema.jsonify(new_usertype)


@app.route('/calidadaire/usertypes', methods=['GET'])
def get_usertypes():
    all_usertypes = UserTypes.query.all()
    result = usertypes_schema.dump(all_usertypes)
    return jsonify(result)


@app.route('/calidadaire/usertypes/<id>', methods=['GET'])
def get_usertype(id):
    usertype = UserTypes.query.get(id)
    return usertype_schema.jsonify(usertype)


# Document Types
class DocTypes(db.Model):
    __tablename__ = 'DOC_TYPES'

    id = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name


class DocTypesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


doctype_schema = DocTypesSchema()
doctypes_schema = DocTypesSchema(many=True)


@app.route('/calidadaire/doctypes', methods=['POST'])
def create_doctypes():
    id = request.json['id']
    name = request.json['name']
    new_doctype = DocTypes(id, name)
    db.session.add(new_doctype)
    db.session.commit()

    return usertype_schema.jsonify(new_doctype)


@app.route('/calidadaire/doctypes', methods=['GET'])
def get_doctypes():
    all_usertypes = DocTypes.query.all()
    result = doctypes_schema.dump(all_usertypes)
    return jsonify(result)


# Particles API 's
class Particles(db.Model):
    __tablename__ = 'PARTICLES'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)

    def __init__(self, name):
        self.name = name


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


# Users API 's

class User(db.Model):
    __tablename__ = 'USERS'

    id = db.Column(db.String(10), primary_key=True)
    idtype = db.Column(db.String(3), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    cel = db.Column(db.String, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    psw = db.Column(db.String(66), nullable=False)
    device = db.Column(db.Integer, nullable=True)
    bdate = db.Column(db.String, nullable=False)
    edate = db.Column(db.String, nullable=False)

    def __init__(self, id, idtype, name, email, cel, type, psw, device, bdate, edate):
        self.id = id
        self.idtype = idtype
        self.name = name
        self.email = email
        self.cel = cel
        self.type = type
        self.psw = self.generate_psw(psw)
        self.device = device
        self.bdate = bdate
        self.edate = edate

    def verify_psw(self, psw):
        return check_password_hash(self.psw, psw)

    def generate_psw(self, psw):
        return generate_password_hash(psw)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'idtype', 'name', 'email', 'cel', 'type', 'psw', 'device', 'bdate', 'edate')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/calidadaire/signup', methods=['POST'])
def create_user():
    today = date.today()
    id = request.json['id']
    idtype = request.json['idtype']
    name = request.json['name']
    email = request.json['email']
    cel = request.json['cel']
    type = request.json['type']
    psw = request.json['psw']
    device = request.json['device']
    bdate = arrow.get(request.json['bdate']).format('YYYY-MM-DD')
    edate = arrow.get(today).format('YYYY-MM-DD')
    new_user = User(id, idtype, name, email, cel, type,
                    psw, device, bdate, edate)

    db.session.add(new_user)
    db.session.commit()
    new_user.psw = ''
    return user_schema.jsonify(new_user)


@app.route('/calidadaire/login', methods=['POST'])
def login_user():
    id = request.json['id']
    psw = request.json['psw']

    user = User.query.filter_by(id=id).first()

    if user is not None and user.verify_psw(psw):
        user.psw = ''
        session['userid'] = user.id
        return user_schema.jsonify(user)
    else:
        response = jsonify({'message': 'Usuario o contraseña invalidos.'})
        response.status_code = 400
        return response


@app.route('/calidadaire/logout', methods=['GET'])
def log_out():
    if 'userid' in session:
        session.pop('userid', None)
        response = jsonify({'message': 'Ha finalizado sesión correctamente.'})
        response.status_code = 200
        return response
    else:
        response = jsonify({'message': 'Ya ha cerrado sesión correctamente'})
        response.status_code = 400
        return response


@app.route('/calidadaire/users', methods=['GET'])
def get_users():
    all_user = User.query.all()
    result = users_schema.dump(all_user)
    return jsonify(result)


@app.route('/calidadaire/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    user.psw = ''
    return user_schema.jsonify(user)


@app.route('/calidadaire/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    response = jsonify({'message': 'Usuario eliminado exitosamente.'})
    response.status_code = 200
    return response


@app.route('/calidadaire/users/selectbydevice/<type>', methods=['GET'])
def get_user_by_type(type):
    records = User.query.filter_by(type=type)
    result = users_schema.dump(records)
    return jsonify(result)


@app.route('/calidadaire/users/<id>/<state>', methods=['PUT'])
def update_user(id, state):
    user = User.query.get(id)

    if state == '0':
        id = request.json['id']
        idtype = request.json['idtype']
        name = request.json['name']
        email = request.json['email']
        cel = request.json['cel']
        type = request.json['type']
        psw = request.json['psw']
        device = request.json['device']
        bdate = arrow.get(request.json['bdate']).format('YYYY-MM-DD')

        user.id = id
        user.idtype = idtype
        user.name = name
        user.email = email
        user.cel = cel
        user.type = type
        user.psw = user.generate_psw(psw)
        user.device = device
        user.bdate = bdate

        db.session.commit()
        user.psw = ''

        return user_schema.jsonify(user)
    if state == '1':
        psw = request.json['psw']
        user.psw = user.generate_psw(psw)
        db.session.commit()

        response = jsonify({'message': 'Se ha cambiado la contraseña exitosamente.'})
        response.status_code = 200
        return response


# Devices API 's
class Devices(db.Model):
    __tablename__ = 'DEVICES'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    geo = db.Column(db.String(30), nullable=False)
    altitude = db.Column(db.Integer)

    def __init__(self, name, geo, altitude):
        self.name = name
        self.geo = geo
        self.altitude = altitude


class DeviceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'geo', 'altitude')


device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)


@app.route('/calidadaire/device', methods=['POST'])
def create_device():
    name = request.json['name']
    geo = request.json['geo']
    altitude = request.json['altitude']
    new_device = Devices(name, geo, altitude)
    db.session.add(new_device)
    db.session.commit()

    return device_schema.jsonify(new_device)


@app.route('/calidadaire/device', methods=['GET'])
def get_devices():
    all_devices = Devices.query.all()
    result = devices_schema.dump(all_devices)
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


# Quality Data
class QualityData(db.Model):
    __tablename__ = 'QUALITY_DATA'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)
    id_particle1 = db.Column(db.Integer, nullable=False)
    value_particle1 = db.Column(db.Integer, nullable=False)
    id_particle2 = db.Column(db.Integer, nullable=False, foreign_key='PARTICLES.id')
    value_particle2 = db.Column(db.Integer, nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    rh = db.Column(db.Integer)
    date = db.Column(db.String, nullable=False, )

    def __init__(self, device, pressure, id_particle1, value_particle1, id_particle2, value_particle2,
                 temp, rh, date):
        self.device = device
        self.pressure = pressure
        self.id_particle1 = id_particle1
        self.value_particle1 = value_particle1
        self.id_particle2 = id_particle2
        self.value_particle2 = value_particle2
        self.temp = temp
        self.rh = rh
        self.date = date


class QualityDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'device', 'pressure', 'id_particle1', 'value_particle1', 'id_particle2', 'value_particle2',
                  'temp', 'rh', 'date')


data_schema = QualityDataSchema()
quality_data_schema = QualityDataSchema(many=True)


@app.route('/calidadaire/qualitydata', methods=['POST'])
def create_record():
    device = request.json['device']
    pressure = request.json['pressure']
    id_particle1 = request.json['id_particle1']
    value_particle1 = request.json['value_particle1']
    id_particle2 = request.json['id_particle2']
    value_particle2 = request.json['value_particle2']
    temp = request.json['temp']
    rh = request.json['rh']
    date = arrow.get(request.json['date']).format('YYYY-MM-DD HH: mm: ss')
    new_record = QualityData(device, pressure, id_particle1, value_particle1, id_particle2, value_particle2,
                             temp, rh, date)

    db.session.add(new_record)
    db.session.commit()
    return data_schema.jsonify(new_record)


@app.route('/calidadaire/qualitydata', methods=['GET'])
def get_records():
    all_records = QualityData.query.all()
    result = quality_data_schema.dump(all_records)
    return jsonify(result)


@app.route('/calidadaire/qualitydata/<id>', methods=['GET'])
def get_record(id):
    record = QualityData.query.get(id)
    return data_schema.jsonify(record)


@app.route('/calidadaire/qualitydata/selectbydevice/<device>', methods=['GET'])
def get_record_by_device(device):
    records = QualityData.query.filter_by(device=device)
    result = quality_data_schema.dump(records)
    return jsonify(result)


@app.route('/calidadaire/qualitydata/<id>', methods=['PUT'])
def update_record(id):
    record = QualityData.query.get(id)

    device = request.json['device']
    pressure = request.json['pressure']
    id_particle1 = request.json['id_particle1']
    value_particle1 = request.json['value_particle1']
    id_particle2 = request.json['id_particle2']
    value_particle2 = request.json['value_particle2']
    temp = request.json['temp']
    rh = request.json['rh']
    date = request.json['date']

    record.device = device
    record.pressure = pressure
    record.id_particle1 = id_particle1
    record.value_particle1 = value_particle1
    record.id_particle2 = id_particle2
    record.value_particle2 = value_particle2
    record.temp = temp
    record.rh = rh
    record.date = date

    db.session.commit()
    return data_schema.jsonify(record)


@app.route('/calidadaire/qualitydata/<id>', methods=['DELETE'])
def delete_record(id):
    record = QualityData.query.get(id)

    db.session.delete(record)
    db.session.commit()

    return data_schema.jsonify(record)


# Log Quality Data
class LogQualityData(db.Model):
    __tablename__ = 'LOG_QUALITY_DATA'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)
    id_particle1 = db.Column(db.Integer, nullable=False)
    value_particle1 = db.Column(db.Integer, nullable=False)
    id_particle2 = db.Column(db.Integer, nullable=False)
    value_particle2 = db.Column(db.Integer, nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    rh = db.Column(db.Integer)
    date = db.Column(db.String, nullable=False)

    def __init__(self, device, pressure, id_particle1, value_particle1, id_particle2, value_particle2,
                 temp, rh, date):
        self.device = device
        self.pressure = pressure
        self.id_particle1 = id_particle1
        self.value_particle1 = value_particle1
        self.id_particle2 = id_particle2
        self.value_particle2 = value_particle2
        self.temp = temp
        self.rh = rh
        self.date = date


db.create_all()


class LogQualityDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'device', 'pressure', 'id_particle1', 'value_particle1', 'id_particle2', 'value_particle2',
                  'temp', 'rh', 'date')


log_data_schema = LogQualityDataSchema()
log_quality_data_schema = LogQualityDataSchema(many=True)


@app.route('/calidadaire/logqualitydata', methods=['POST'])
def create_log_record():
    device = request.json['device']
    pressure = request.json['pressure']
    id_particle1 = request.json['id_particle1']
    value_particle1 = request.json['value_particle1']
    id_particle2 = request.json['id_particle2']
    value_particle2 = request.json['value_particle2']
    temp = request.json['temp']
    rh = request.json['rh']
    date = arrow.get(request.json['date']).format('YYYY-MM-DD HH: mm: ss')

    new_logrecord = LogQualityData(device, pressure, id_particle1, value_particle1, id_particle2, value_particle2,
                                   temp, rh, date)

    db.session.add(new_logrecord)
    db.session.commit()

    return log_data_schema.jsonify(new_logrecord)


@app.route('/calidadaire/logqualitydata', methods=['GET'])
def get_log_records():
    all_logrecords = LogQualityData.query.all()
    result = log_quality_data_schema.dump(all_logrecords)
    return jsonify(result)


@app.route('/calidadaire/logqualitydata/<id>', methods=['GET'])
def get_log_record(id):
    logrecord = LogQualityData.query.get(id)
    return log_data_schema.jsonify(logrecord)


@app.route('/calidadaire/logqualitydata/selectbydevice/<device>', methods=['GET'])
def get_log_record_by_device(device):
    records = LogQualityData.query.filter_by(device=device)
    result = log_quality_data_schema.dump(records)
    return jsonify(result)


@app.route('/calidadaire/logqualitydata/<id>', methods=['PUT'])
def update_log_record(id):
    logrecord = LogQualityData.query.get(id)

    device = request.json['device']
    pressure = request.json['pressure']
    id_particle1 = request.json['id_particle1']
    value_particle1 = request.json['value_particle1']
    id_particle2 = request.json['id_particle2']
    value_particle2 = request.json['value_particle2']
    temp = request.json['temp']
    rh = request.json['rh']
    date = request.json['date']

    logrecord.device = device
    logrecord.pressure = pressure
    logrecord.id_particle1 = id_particle1
    logrecord.value_particle1 = value_particle1
    logrecord.id_particle2 = id_particle2
    logrecord.value_particle2 = value_particle2
    logrecord.temp = temp
    logrecord.rh = rh
    logrecord.date = date

    db.session.commit()
    return log_data_schema.jsonify(logrecord)


@app.route('/calidadaire/logqualitydata/<id>', methods=['DELETE'])
def delete_log_record(id):
    logrecord = LogQualityData.query.get(id)

    db.session.delete(logrecord)
    db.session.commit()

    return log_data_schema.jsonify(logrecord)


if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)
