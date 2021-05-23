import arrow
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask('__flask__')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1qaw3edr5tg@192.168.1.102:9000/calidadaireDB'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    id_particle2 = db.Column(db.Integer, nullable=False)
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
    records = QualityData.query.get(device)
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
    logrecords = LogQualityData.query.get(device)
    result = log_quality_data_schema.dump(logrecords)
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
    app.run()
