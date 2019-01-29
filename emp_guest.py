import numpy as np


#1. create a data structure which acts as a employee database (ID, username, password, firstname)
#2. evaluate the user with his username and password
#3. Give three chances to the user

guest_db = {}
guest_ids = np.arange(1,1000)
#global run_guest
run_guest =1
def guest_id(run):
    return guest_ids[run]

def evaluate(**kwargs):
    if 'employee' == kwargs['type']:
        employee_id = kwargs['id']
        password = kwargs['password']
        employee_db = {12345:['robert','robert@2019','Robert'], 12346:['arthur','arthur@2019','Arthur'], 12347:['cobb','cobb@2019', 'Cobb'],12348:['bruce','bruce@2019','Bruce'],
                   12349:['ariadne','ariadne@2019','Ariadne']}
        if employee_id in employee_db.keys():
            if password == employee_db[employee_id][1]:
                return True
            else:
                return False
        else:
            return 'Please check your ID'
    elif 'guest' == kwargs['type']:
        global run_guest
        run_guest+=1
        name = kwargs['name']
        email = kwargs['email']

        # generate a guest id
        guest_id_num = guest_id(run_guest)
        guest_db[guest_id_num]=[name,email]
        return 'guest added'









#print(evaluate(12343,'arthur@2019'))
print(evaluate(**{'type':'guest','name':'saito','email':'saito@gmail.com'}))
print(evaluate(**{'type':'employee', 'id': 12345 ,'password': 'robert@2019'}))