import uuid
from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
import requests
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testw'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Employee(db.Model):
    # __tablename__='employee'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    # str conversion for mysql
    name = db.Column('name', db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'phone_number': self.phone_number}

    def __repr__(self):
        # return f"Employee(id:{self.id}, name={self.name}, phone_number={self.phone_number}, email={self.email})"
        return f"id:{self.id}, name={self.name}, phone_number={self.phone_number}, email={self.email}"


with app.app_context():
    db.create_all()


api_key = "8aa46341f09c625169029d3dd37c3220"


def weather(city):
    response = requests.get(" https://api.openweathermap.org/data/2.5/weather?q="
                            + city
                            + "&units=metric&appid="
                            + api_key)
    return json.loads(response.content)


@app.route("/")
def welcome():
    # [{"id": 1, "name": "abel"}, {"id": 2, "name": "bekele"}]
    parse_data = Employee.query.all()
    # data = get().get_data()
    # # as_text=True
    # parse_data = json.loads(data)
    # print(parse_data)
    return render_template("index.html", data=parse_data)


@app.route("/Weather")
def test():
    return render_template("weather.html", weather=weather('London'))


@app.route("/base")
def base():
    return render_template('base.html')


# crud

@app.route("/employees", methods=['POST'])
def create():
    data = None
    email = None
    name = None
    phone_number = None
    try:
        data = request.get_json()
        email = data['email']
        name = data['name']
        phone_number = data['phone_number']

        employee1 = Employee.query.filter(Employee.email == email).all()
        # print(employee)
        if employee1:
            return (jsonify({'error': 'user already exists'}), 409)
        # 409 conflict
        else:
            try:
                employee = Employee(
                    name=name, phone_number=phone_number, email=email)
                # return employee.__dir__()
                db.session.add(employee)
                db.session.commit()
                print(employee)
                model = employee.__dict__
                print(model)
                model.pop('_sa_instance_state')
                print(model)
                return jsonify(model), 201
            except Exception as e:
                return e

    except Exception as error:
        data = request.form
        print(data, type(data))
        email = data['email']
        name = data['name']
        phone_number = data['phone_number']

        employee1 = Employee.query.filter(Employee.email == email).all()
        # print(employee)
        if employee1:
            flash(['!!!!!!!user already exists', 'alert-success'])
            return redirect(url_for('welcome'))
            # return (jsonify({'error': 'user already exists'}), 409)
        # 409 conflict
        else:
            try:
                employee = Employee(
                    name=name, phone_number=phone_number, email=email)
                # return employee.__dir__()
                db.session.add(employee)
                db.session.commit()
                print(employee)
                model = employee.__dict__
                print(model)
                model.pop('_sa_instance_state')
                print(model)
                flash(['user created', 'alert-success'])
                return redirect(url_for('welcome'))
                return jsonify(model), 201
            except Exception as e:
                return e


@app.route("/employees", methods=['GET'])
def get():
    emps = [emp.__dict__ for emp in Employee().query.all()]
    for emp in emps:
        emp.pop('_sa_instance_state')
    # print(emps)
    return jsonify(emps)


@app.route("/employees/<id>", methods=['GET'])
def get_one(id):
    try:
        employee = Employee().query.filter(Employee.id == id).one()
        # employee= Employee.query.get(id)
        print(employee)
        if employee:
            employee = employee.__dict__
            employee.pop('_sa_instance_state')
            return jsonify(employee), 200
        else:
            return jsonify({'error': 'Not Found'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/employees/<id>", methods=['PUT','POST'])
def update(id):
    data = None
    # email = None
    name = None
    phone_number = None
    try:
        data = request.get_json()
        # email = data['email']
        name = data['name']
        phone_number = data['phone_number']

        employee = Employee().query.get(id)

        if employee:
            employee.phone_number = phone_number
            employee.name = name
            db.session.commit()
            flash(['user Updated', 'alert-success'])
            return redirect(url_for('welcome'))
            # return redirect(url_for('get', id=id))
        else:
            return 'Not Found', 201
    except Exception as error:
        data = request.form
        print(data, type(data))
        email = data['email']
        name = data['name']
        phone_number = data['phone_number']
        employee = Employee().query.get(id)
        if employee:
            employee.phone_number = phone_number
            employee.name = name
            db.session.commit()
            flash(['user Updated', 'alert-success'])
            return redirect(url_for('welcome'))
            # return redirect(url_for('get', id=id))
        else:
            flash(['!!!!!!!user Not Found', 'alert-success'])
            return redirect(url_for('welcome'))
            # return 'Not Found', 201

    


@app.route("/employee/<id>", methods=['DELETE','POST'])
def delete(id):
    employee = Employee().query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash(['deleted'])
        return redirect(url_for('welcome'))
        return 'Deleted', 200
    else:
        flash(['Not Found'])
        return redirect(url_for('welcome'))
        return 'Not Found', 201


if __name__ == "__main__":
    app.run(host="0.0.0.0",  port=3003)
