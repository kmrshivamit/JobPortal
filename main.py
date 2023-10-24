from flask import Flask,request,url_for,jsonify
from Model.employee import Employee
from utils.db import DataBase 
from datetime import datetime

date_format = "%Y/%m/%d %H:%M:%S"

db=DataBase('root','root','localhost','recruitment_portal',ssl_ca=None,charset="utf8mb4"
   )
# import jsonify
employees = [
    Employee("user1", "pass123", "John", "Doe", "123 Main St", "ABC Inc", "5", ["Java", "Python", "SQL"],"C1",1)
]

app=Flask(__name__)

@app.route('/AddEmployee',methods=['POST'])
def add_employee():
    
    data = request.get_json()  # Parse JSON data from the request body
    user_name = data.get('user_name')
    if db.is_existing_username(user_name):
                return jsonify({'message': 'User with the same user_name already exists'})

        
    
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')
    company = data.get('company')
    # datetime_object = datetime.strptime(date_string, date_format)

    date_of_joining = datetime.strptime(data.get('date_of_joining'),date_format)
    skills = str(data.get('skills'))
    salary_grade=data.get('salary_grade')
    is_active=data.get('is_active')
    
    new_employee = Employee( user_name, password, first_name, last_name, address, company, date_of_joining, skills,salary_grade,is_active)
    
    employees.append(new_employee)
    
    db.add_employee(new_employee)
    
    return jsonify({'message': 'User added successfully','emp':str(new_employee)})

@app.route("/DisplayEmployees",methods=['POST'])
def display_employee():
    employees=db.view_employee()
    employees_data= [ employee.to_json() for employee in employees]
    return jsonify(employees_data)

@app.route("/DeleteEmployee", methods=['POST'])
def delete_employee():
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')
    deleted=db.remove_employee(user_name,password)
    if deleted:
         return jsonify({'message': 'Employee deleted successfully'})
    else :
        return jsonify({'message':'Employee does not exists with the given username or password'})
    

@app.route("/UpdateEmployee",methods=['POST'])
def update_employee():
    data=request.get_json()
    keys=data.keys()
    print(keys)
    if ('user_name'  in keys) and ('password' in keys):
        user_exists=db.is_existing_username_password(data['user_name'],data['password'])
        if user_exists==None:
            return jsonify({'message':'Username does not exist'})
        if user_exists==False:
            return jsonify({'message':'password is wrong'})
        db.update_employee(data)
        return jsonify({'msg':'employee successfully updated with new' + str(keys)})
    else:
        return jsonify({'msg':"username or password is missing"})
            
if __name__=='__main__':  
    app.run(debug=True)