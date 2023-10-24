
class Employee:
    def __init__(self, user_name, password, first_name, last_name, address, company, date_of_joining, skills,salary_grade,is_active):
        self._user_name = user_name
        self._password = password
        self._first_name = first_name
        self._last_name = last_name
        self._address = address
        self._company = company
        self._date_of_joining = date_of_joining
        self._skills = skills
        self._salary_grade=salary_grade
        self._is_active=is_active
        
         

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        self._user_name = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, value):
        self._company = value

    @property
    def date_of_joining(self):
        return self._date_of_joining

    @date_of_joining.setter
    def date_of_joining(self, value):
        self._date_of_joining = value

    @property
    def skills(self):
        return self._skills

    @skills.setter
    def skills(self, value):
        self._skills = value
    
    @property
    def is_active(self):
        return self._is_active
    
    @is_active.setter
    def is_active(self,value):
         self._is_active=value

    def __str__(self):
        return f"Employee: {self._first_name} {self.last_name}, User: {self.user_name}, Company: {self.company}, Skills:{self.skills}, Is_Active:{self.is_active}"
    
    def to_json(self):
        return {"user_name": self.user_name,
        "password": self.password,
        "first_name": self.first_name,
        "last_name":self.last_name,
        "address" :self.address,
        "company":self.company,
        "date_of_joining":self.date_of_joining,
        "skills":self.skills ,
        "salary_grade":self._salary_grade ,
        "is_active":self.is_active 
        }

    @property
    def salary_grade(self):
        return self._salary_grade

    @salary_grade.setter
    def salary_grade(self,grade):
        self._grade=grade

        
        
if __name__=="__main__":
    e=Employee('kmrshivamit', "Shivam@12345", 
                   "Kumar", "Shivam", "Darbhanga", "LTIMindtree", '22/08/2024', ['python','Java','Spark'],'C1',1)
    e.grade='C3'
    print(e.grade)