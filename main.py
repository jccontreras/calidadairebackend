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
# Configuración para la conexión a la base de datos (BD)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ragnarok000:1qaw3edr5tg@ragnarok000.mysql.pythonanywhere-services.com/ragnarok000$calidadaireueb'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
PORT = 5000
DEBUG = False
app.secret_key = '5HnNaFgcBVNxkUswJ74eImPJQuXSvecr'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Url que redirecciona a archivo swagger
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


# User Types - Creación y/o referenciación de tabla USER_TYPES en la BD
class UserTypes(db.Model):
    __tablename__ = 'USER_TYPES'

    # Columnas de la tabla USER_TYPES en la BD
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name


class UserTypesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


usertype_schema = UserTypesSchema()  # Esquema para un tipo de usuario
usertypes_schema = UserTypesSchema(many=True)  # Esquema para muchos tipos de usuario


# USER_TYPES API's

# Inserta un nuevo tipo de usuario en la BD
@app.route('/calidadaire/usertypes', methods=['POST'])
def create_usertypes():
    if 'userid' in session:  # Verifica si hay una sesión iniciada.
        name = request.json['name']
        new_usertype = UserTypes(name)
        db.session.add(new_usertype)
        db.session.commit()
        return usertype_schema.jsonify(new_usertype)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene todos los tipos de usuario de la BD
@app.route('/calidadaire/usertypes', methods=['GET'])
def get_usertypes():
    all_usertypes = UserTypes.query.all()
    result = usertypes_schema.dump(all_usertypes)
    return jsonify(result)


# Obtiene un tipo de usuario específico de la BD
@app.route('/calidadaire/usertypes/<id>', methods=['GET'])
def get_usertype(id):
    usertype = UserTypes.query.get(id)
    return usertype_schema.jsonify(usertype)


# Document Types - Creación y/o referenciación de tabla DOC_TYPES en la BD
class DocTypes(db.Model):
    __tablename__ = 'DOC_TYPES'

    # Columnas de la tabla DOC_TYPES en la BD
    id = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name


class DocTypesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


doctype_schema = DocTypesSchema()  # Esquema para un tipo de documento
doctypes_schema = DocTypesSchema(many=True)  # Esquema para muchs tipos de documento


# DOC_TYPES API's

# Inserta tipos de documentos en la BD
@app.route('/calidadaire/doctypes', methods=['POST'])
def create_doctypes():
    id = request.json['id']
    name = request.json['name']
    new_doctype = DocTypes(id, name)
    db.session.add(new_doctype)
    db.session.commit()

    return usertype_schema.jsonify(new_doctype)


# Obtiene los tipos de documento de la BD
@app.route('/calidadaire/doctypes', methods=['GET'])
def get_doctypes():
    all_usertypes = DocTypes.query.all()
    result = doctypes_schema.dump(all_usertypes)
    return jsonify(result)


# Particles - Creación y/o referenciación de tabla PARTICLES en la BD
class Particles(db.Model):
    __tablename__ = 'PARTICLES'

    # Columnas de la tabla PARTICLES en la BD
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)

    def __init__(self, name):
        self.name = name


class ParticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


particle_schema = ParticleSchema()  # Esquema para una partícula
particles_schema = ParticleSchema(many=True)  # Esquema para muchas partículas


# PARTICLES API's

# Inserta una nueva partícula en la BD
@app.route('/calidadaire/particles', methods=['POST'])
def create_particle():
    if 'userid' in session:
        name = request.json['name']
        new_particle = Particles(name)
        db.session.add(new_particle)
        db.session.commit()

        return particle_schema.jsonify(new_particle)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene todas las partícula de la BD
@app.route('/calidadaire/particles', methods=['GET'])
def get_particles():
    all_particles = Particles.query.all()
    result = particles_schema.dump(all_particles)
    return jsonify(result)


# Obtiene una partícula en específico de la BD
@app.route('/calidadaire/particle/<id>', methods=['GET'])
def get_particle(id):
    particle = Particles.query.get(id)
    return particle_schema.jsonify(particle)


# Actualiza una partícula en la BD
@app.route('/calidadaire/particle/<id>', methods=['PUT'])
def update_particle(id):
    if 'userid' in session:
        particle = Particles.query.get(id)
        name = request.json['name']
        particle.name = name
        db.session.commit()
        return particle_schema.jsonify(particle)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Elimina una partícula en la BD
@app.route('/calidadaire/particle/<id>', methods=['DELETE'])
def delete_particle(id):
    if 'userid' in session:
        particle = Particles.query.get(id)
        db.session.delete(particle)
        db.session.commit()
        return particle_schema.jsonify(particle)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Users - Creación y/o referenciación de tabla USERS en la BD
class User(db.Model):
    __tablename__ = 'USERS'

    # Columnas de la tabla USERS en la BD
    id = db.Column(db.String(10), primary_key=True)
    idtype = db.Column(db.String(3), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    cel = db.Column(db.String(12), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    psw = db.Column(db.String(66), nullable=False)
    device = db.Column(db.Integer, nullable=True)
    bdate = db.Column(db.String(20), nullable=False)
    edate = db.Column(db.String(20), nullable=False)

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

    # Método para verificar el psw de un usuario a la hora de iniciar sesión
    def verify_psw(self, psw):
        return check_password_hash(self.psw, psw)

    # Método para generar el hash sha256 del psw del usuario antes de registrarlo en la BD
    def generate_psw(self, psw):
        return generate_password_hash(psw)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'idtype', 'name', 'email', 'cel', 'type', 'psw', 'device', 'bdate', 'edate')


user_schema = UserSchema()  # Esquema para un usuario
users_schema = UserSchema(many=True)  # Esquema para muchos usuarios


# USERS API's

# Inserta un nuevo usuario en la BD
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


# Inicia sesión de un usuario en el sistema
@app.route('/calidadaire/login', methods=['POST'])
def login_user():
    id = request.json['id']
    psw = request.json['psw']

    user = User.query.filter_by(id=id).first()

    if user is not None and user.verify_psw(psw):  # Verifica que el usuario exista y que la contraseña coincida
        user.psw = ''
        session['userid'] = user.id  # Inicia la session
        return user_schema.jsonify(user)
    else:
        response = jsonify({'message': 'Usuario o contraseña invalidos.'})
        response.status_code = 400
        return response


# Cierra la sesión de un usuario en el sistema
@app.route('/calidadaire/logout', methods=['GET'])
def log_out():
    if 'userid' in session:  # Verifica si hay una sesión iniciada.
        session.pop('userid', None)  # Finaliza la session
        response = jsonify({'message': 'Ha finalizado sesión correctamente.'})
        response.status_code = 200
        return response
    else:
        response = jsonify({'message': 'Ya ha cerrado sesión correctamente'})
        response.status_code = 400
        return response


# Obtiene todos los usuario de la BD
@app.route('/calidadaire/users', methods=['GET'])
def get_users():
    if 'userid' in session:
        all_user = User.query.all()
        result = users_schema.dump(all_user)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene un usuario específico filtrado por id de la BD
@app.route('/calidadaire/users/<id>', methods=['GET'])
def get_user(id):
    if 'userid' in session:
        user = User.query.get(id)
        user.psw = ''
        return user_schema.jsonify(user)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Elimina un usuario de la BD
@app.route('/calidadaire/users/<id>', methods=['DELETE'])
def delete_user(id):
    if 'userid' in session:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        response = jsonify({'message': 'Usuario eliminado exitosamente.'})
        response.status_code = 200
        return response
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene una lista de usuarios filtrados por el tipo de usuario de la BD
@app.route('/calidadaire/users/selectbytype/<type>', methods=['GET'])
def get_user_by_type(type):
    if 'userid' in session:
        records = User.query.filter_by(type=type)
        result = users_schema.dump(records)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Si se es administrador actualiza los datos de un usuario específico,
# Si es otro tipo de usuario actualiza su contraseña.
@app.route('/calidadaire/users/<id>/<state>', methods=['PUT'])
def update_user(id, state):
    user = User.query.get(id)

    if state == '0':  # Entra si el usuario es administrador del sistema
        if 'userid' in session:
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
        else:
            response = jsonify({'message': 'Debe tener su sesión iniciada.'})
            response.status_code = 400
            return response
    if state == '1':  # Entra si es un usuario no administrador
        psw = request.json['psw']
        user.psw = user.generate_psw(psw)
        db.session.commit()

        response = jsonify({'message': 'Se ha cambiado la contraseña exitosamente.'})
        response.status_code = 200
        return response


# Devices - Creación y/o referenciación de tabla DEVICES en la BD
class Devices(db.Model):
    __tablename__ = 'DEVICES'

    # Columnas de la tabla DEVICES en la BD
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


device_schema = DeviceSchema()  # Esquema para un dispositivo
devices_schema = DeviceSchema(many=True)  # Esquema para muchos dispositivos


# DEVICES API's

# Inserta un dispositivo en la BD
@app.route('/calidadaire/device', methods=['POST'])
def create_device():
    name = request.json['name']
    geo = request.json['geo']
    altitude = request.json['altitude']
    new_device = Devices(name, geo, altitude)
    db.session.add(new_device)
    db.session.commit()

    return device_schema.jsonify(new_device)


# Obtiene los dispositivos de la BD
@app.route('/calidadaire/device', methods=['GET'])
def get_devices():
    if 'userid' in session:
        all_devices = Devices.query.all()
        result = devices_schema.dump(all_devices)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene un dispositivo específico de la BD
@app.route('/calidadaire/device/<id>', methods=['GET'])
def get_device(id):
    if 'userid' in session:
        particle = Devices.query.get(id)
        return device_schema.jsonify(particle)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Actualiza los datos de un dispositivo específico en la BD
@app.route('/calidadaire/device/<id>', methods=['PUT'])
def update_device(id):
    if 'userid' in session:
        device = Devices.query.get(id)
        name = request.json['name']
        geo = request.json['geo']
        altitude = request.json['altitude']

        device.name = name
        device.geo = geo
        device.altitude = altitude

        db.session.commit()
        return device_schema.jsonify(device)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Elimina un dispositivo en la BD
@app.route('/calidadaire/device/<id>', methods=['DELETE'])
def delete_device(id):
    if 'userid' in session:
        device = Devices.query.get(id)
        db.session.delete(device)
        db.session.commit()
        return device_schema.jsonify(device)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Quality Data - Creación y/o referenciación de tabla QUALITY_DATA en la BD
class QualityData(db.Model):
    __tablename__ = 'QUALITY_DATA'

    # Columnas de la tabla QUALITY_DATA en la BD
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


data_schema = QualityDataSchema()  # Esquema para un registro de calidad del aire
quality_data_schema = QualityDataSchema(many=True)  # Esquema para muchos registros de calidad del aire


# QUALITY_DATA API's

# Inserta registro de calidad del aire en la BD
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
    date = arrow.get(request.json['date']).format('YYYY-MM-DD HH:mm:ss')
    new_record = QualityData(device, pressure, id_particle1, value_particle1, id_particle2, value_particle2,
                             temp, rh, date)

    db.session.add(new_record)
    db.session.commit()
    return data_schema.jsonify(new_record)


# Obtiene todos los registros de calidad del aire de la BD
@app.route('/calidadaire/qualitydata', methods=['GET'])
def get_records():
    if 'userid' in session:
        all_records = QualityData.query.all()
        result = quality_data_schema.dump(all_records)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene un registro específico de calidad del aire de la BD
@app.route('/calidadaire/qualitydata/<id>', methods=['GET'])
def get_record(id):
    if 'userid' in session:
        record = QualityData.query.get(id)
        return data_schema.jsonify(record)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obiene los registros de calidad del aire filtrados por dispositivo de la BD
@app.route('/calidadaire/qualitydata/selectbydevice/<device>', methods=['GET'])
def get_record_by_device(device):
    if 'userid' in session:
        records = QualityData.query.filter_by(device=device)
        result = quality_data_schema.dump(records)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obiene los registros de calidad del aire filtrados por usuario de la BD
@app.route('/calidadaire/qualitydata/selectbyuser/<userid>', methods=['GET'])
def get_record_by_user(userid):
    if 'userid' in session:
        user = User.query.get(userid)
        records = QualityData.query.filter_by(device=user.device)
        result = quality_data_schema.dump(records)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obiene los registros de calidad del aire filtrados por fecha (año, mes, día, hora y/o minuto) de la BD
@app.route('/calidadaire/qualitydata/datefilter', methods=['POST'])
def get_record_by_date():
    if 'userid' in session:
        year = request.json['year']
        month = request.json['month']
        day = request.json['day']
        hour = request.json['hour']
        min = request.json['min']

        date = ''
        if year != '':
           date = year
        if month != '':
            date += '-' + month
        if day != '':
            date += '-' + day + ' '
        if hour != '':
            date += hour + ':'
        if min != '':
            date += min

        date += '%'

        records = QualityData.query.filter(QualityData.date.like(date))
        result = quality_data_schema.dump(records)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Actualiza un registro específico de calidad del aire en la BD
@app.route('/calidadaire/qualitydata/<id>', methods=['PUT'])
def update_record(id):
    if 'userid' in session:
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
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Elimina un registro de calidad del aire en la BD
@app.route('/calidadaire/qualitydata/<id>', methods=['DELETE'])
def delete_record(id):
    if 'userid' in session:
        record = QualityData.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return data_schema.jsonify(record)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Log Quality Data - Creación y/o referenciación de tabla LOG_QUALITY_DATA en la BD
class LogQualityData(db.Model):
    __tablename__ = 'LOG_QUALITY_DATA'

    # Columnas de la tabla LOG_QUALITY_DATA en la BD
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



class LogQualityDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'device', 'pressure', 'id_particle1', 'value_particle1', 'id_particle2', 'value_particle2',
                  'temp', 'rh', 'date')


log_data_schema = LogQualityDataSchema()  # Esquema de un registro log de calidad del aire
log_quality_data_schema = LogQualityDataSchema(many=True)  # Esquema de muchos registros log de calidad del aire


# LOG_QUALITY_DATA API's

# Inserta un registro log de calidad del aire en la BD
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


# Obtiene los registros log de calidad del aire de la BD
@app.route('/calidadaire/logqualitydata', methods=['GET'])
def get_log_records():
    if 'userid' in session:
        all_logrecords = LogQualityData.query.all()
        result = log_quality_data_schema.dump(all_logrecords)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene un registro log específico de calidad del aire de la BD
@app.route('/calidadaire/logqualitydata/<id>', methods=['GET'])
def get_log_record(id):
    if 'userid' in session:
        logrecord = LogQualityData.query.get(id)
        return log_data_schema.jsonify(logrecord)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Obtiene un registro log específico de calidad del aire filtrado por dispositivo de la BD
@app.route('/calidadaire/logqualitydata/selectbydevice/<device>', methods=['GET'])
def get_log_record_by_device(device):
    if 'userid' in session:
        records = LogQualityData.query.filter_by(device=device)
        result = log_quality_data_schema.dump(records)
        return jsonify(result)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Actualiza un registro log de calidad del aire en la BD
@app.route('/calidadaire/logqualitydata/<id>', methods=['PUT'])
def update_log_record(id):
    if 'userid' in session:
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
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Elimina un registro log de calidad del aire en la BD
@app.route('/calidadaire/logqualitydata/<id>', methods=['DELETE'])
def delete_log_record(id):
    if 'userid' in session:
        logrecord = LogQualityData.query.get(id)
        db.session.delete(logrecord)
        db.session.commit()
        return log_data_schema.jsonify(logrecord)
    else:
        response = jsonify({'message': 'Debe tener su sesión iniciada.'})
        response.status_code = 400
        return response


# Método main que inicia el sistema
if __name__ == '__main__':
    db.create_all()
    app.run(port=PORT, debug=DEBUG)
