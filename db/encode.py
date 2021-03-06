from db.models import Model, User, Employee, App, Role, Group, EmployeeToRole, RoleToGroup
from db import query
import json


def get_json(name, value, exclude = []):
    obj = None
    if isinstance(value, Model):
        obj = value.get_dict(exclude)
    elif isinstance(value, list):
        obj = [val.get_dict(exclude) for val in value]
    else:
        raise TypeError("get_json() recieved unexpected type for argument",
                        "%s: %s" % ("value", type(value)) )
        
    return json.dumps({name: obj})


def create_error(error, exception = None):
    response = {'error': error}
    
    if exception:
        response['message'] = str(exception)
        
    return json.dumps(response)


def get_employees_json():
    result = query.get_all_employees()
    return get_json('employees', result)