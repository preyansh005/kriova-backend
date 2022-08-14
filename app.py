from flask import *
from flask_sqlalchemy import *
from sqlalchemy.dialects.sqlite import BLOB
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from alerts import EmailAlerts

app = Flask(__name__)
CORS(app)
app.secret_key = '565b5551edbcd1eedce39c68022bb7111c2f714460640ce5934df85743b872ac'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/kriova_assessment'

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    employee_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False)
    mno = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    pincode = db.Column(db.String(50))
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(50))

@app.route('/employee/registration', methods=['POST'])
def create_employee():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = Employee(employee_id = str(uuid.uuid4()), name=data['name'], email=data['email'], mno=data['mno'], password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg':'Employee Registration Successfully'})

@app.route('/employee/login', methods=['GET'])
def find_employee():
    email = request.args.get('email')
    getpassword = request.args.get('password')
    try:
        employee = Employee.query.filter_by(email=email).first()
        if check_password_hash(employee.password,getpassword):
            employee_data={}
            employee_data['employee_id'] = employee.employee_id
            employee_data['name'] = employee.name
            employee_data['mno'] = employee.mno
            employee_data['email'] = employee.email
            employee_data['dob'] = employee.dob
            employee_data['role'] = employee.role
            employee_data['address'] = f"{employee.street}, {employee.city}, {employee.state}, {employee.country}-{employee.pincode}"
        return jsonify({'employee':employee_data,'msg':'Employee Found'})
    except:
        return jsonify({'msg':'Employee Not Found'})

@app.route('/employee/reset', methods=['GET','POST'])
def reset_employee():
    if request.method == 'POST':
        data1 = request.get_json()
        employee = Employee.query.filter_by(employee_id=data1['employee_id']).first()
        hashed_password = generate_password_hash(data1['password'])
        employee.password = hashed_password
        db.session.commit()
        return jsonify({'msg':'Password changed successfully'})
    else:
        email = request.args.get('email')
        try:
            employee = Employee.query.filter_by(email=email).first()
            details = {}
            otp = EmailAlerts.email_otp(employee.email)
            email_id = employee.employee_id
            details['otp'] = otp
            details['employee_id'] = email_id
            return jsonify({'details':details,'msg':'Employee Found'})
        except:
            return jsonify({'msg':'Employee Not Found'})

@app.route('/employee/<email>', methods=['GET'])
def get_all_employee(email):
    try:
        employee = Employee.query.filter_by(email=email).first()
        employee_data={}
        employee_data['employee_id'] = employee.employee_id
        employee_data['name'] = employee.name
        return jsonify({'employee':employee_data,'msg':'Employee Found'})
    except:
        return jsonify({'msg':'Employee Not Found'})

@app.route('/employee/<employee_id>', methods=['GET'])
def get_one_employee(employee_id):
    employee = Employee.query.filter_by(employee_id=employee_id).first()
    if not employee:
        return jsonify({'msg':'No User Found'})
    employee_data={}
    employee_data['employee_id'] = employee.employee_id
    employee_data['name'] = employee.name
    return jsonify({'employee':employee_data})


if __name__ == '__main__':
    app.run(debug=True)