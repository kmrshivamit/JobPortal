from datetime import datetime,timedelta
import os
import logging
import pytz
import numpy as np
import pandas as pd
import json


from sqlalchemy import create_engine,MetaData
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


from Model.employee import Employee

logger=logging.getLogger("prism")
utc_timezone=pytz.utc

class DataBase:
    def __init__(
        self,username,password,host,db_name,ssl_ca=None,charset="utf8mb4"
    ):
        self.engine_url="mysql+mysqldb://{}:{}@{}/{}".format(
            username,password,host,db_name
        )
        if charset is not None:
            self.connect_args={"charset":charset}
        else:
            self.connect_args={}
        if ssl_ca:
            self.connect_args["ssl"]={"ca":ssl_ca}
        self.metadata=MetaData()
        self.engine=create_engine(
            self.engine_url,pool_recycle=500,connect_args=self.connect_args or {}
            
        )
        self.metadata.reflect(
            self.engine,
            only=[ 'employees'],
        )
        self.base=automap_base(metadata=self.metadata)
        self.base.prepare()
        self.employees=self.base.classes.employees
        
    def get_session(self):
        return Session(self.engine)
    def close(self):
        return self.engine.dispose()
    
    def is_existing_username(self, username):
        try:
            with self.get_session() as session:
                print(username)
                # Check if the user_name already exists in the database
                is_exist = session.query(self.employees).filter(self.employees.user_name.in_([username])).first()
                # print(is_exist)
                return bool(is_exist)

        except Exception as e:
            logger.error(f"Issue in verifying if user_name already exists: {e}", exc_info=True)
            return False  # Return False in case of an error
        
    def add_employee(self,emp:Employee):
        row=self.employees()
        row.user_name = emp.user_name
        row.password = emp.password
        row.first_name = emp.first_name
        row.last_name = emp.last_name
        row.address = emp.address
        row.company = emp.company
        row.date_of_joining = emp.date_of_joining
        row.skills = emp.skills
        row.salary_grade=emp.salary_grade
        
        session=self.get_session()
        try:
            session.add(row)
            session.commit()
        except Exception as e:
            logger.error("Issue in adding objects",exc_info=True)
            session.rollback()
        finally:
            session.close()
            
    def is_existing_username_password(self,user_name,password):
        try:
            with self.get_session() as session:
                print(user_name)
                # Check if the user_name already exists in the database
                user = session.query(self.employees).filter(self.employees.user_name.in_([user_name])).first()
                if(user.password==password):
                    return True
                return user
        except Exception as e:
            logger.error(f"Issue in verifying if user_name already exists: {e}", exc_info=True)
            return False  # Return False in case of an error
    def update_employee(self,data):
        try:
            with self.get_session() as session:
                # Check if the user_name already exists in the database
                user = session.query(self.employees).filter(self.employees.user_name.in_([data['user_name']])).first()
                if(user.password==data['password']):
                      for key in data.keys():
                          user.key=key
                session.add(user)
                session.commit()
                return True
                 
        except Exception as e:
            logger.error(f"Issue in verifying if user_name already exists: {e}", exc_info=True)
            return False  # Return False in case of an error
        
    def remove_employee(self,user_name,password):
            try:
                with self.get_session as session:
                        user = session.query(self.employees).filter(self.employees.user_name.in_(['user_name'])).first()
                        if(user is not None and (user.password==password)):
                            user.is_active=0       
                            session.add(user)
                            session.commit()
                            return True
                        return False
            except Exception as e:
                logger.error(f"Error while deleting user")
        
    def view_employee(self):
        users_list=[]
        try:
            with self.get_session() as session:
                users=session.query(self.employees)
                for user in users:
                    users_list.append(Employee(user.user_name,user.password,user.first_name,user.last_name,user.address,user.company,user.date_of_joining,user.skills,user.salary_grade,user.is_active))
                return users_list
                      

                       
        except Exception as e:
            logger.error(f"Error while reading records from db",e)
            
        
        
                
                
                
        
        
        
            
            
        
        
        
        