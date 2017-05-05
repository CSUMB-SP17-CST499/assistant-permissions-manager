from flask import Blueprint, request
from db.encode import get_json, create_error
from db import query
from db.models import Role,Group
import json

roles = Blueprint('roles', __name__,
                    template_folder='templates')

@roles.route('/api/role', methods = ['GET', 'PUT', 'DELETE'])
def role_uri():
    args = request.args
    print(request.get_json())
    args = request.get_json()
    
    
    if args is None:
        response = create_error('missing_argument')
        return (response, 404)
    
    role_id = args.get('id')
    if request.method == 'GET':
        try:
            role = query.get_role_by_id(role_id)
            
            if role:
                return get_json('role', role)
            else:
                response = create_error('role_not_found')
                return (response, 404)
                
        except Exception as e:
            response = create_error('unexpected_error', e)
            return (response, 500)
            
    elif request.method == 'PUT':
        try:
            name = args.get('name')
            description = args.get('description')
            
            # Update the role with the provided info
            if role_id:
                role = query.get_role_by_id(role_id)
                if role:       
                    if query.does_role_name_exist(name):
                        response = create_error('name_taken')
                        return (response, 400)

                    if name:
                        role.name = name
                    if description:
                        role.description = description
                    
                    is_updated = query.update_role(role)
                    if is_updated:
                        return (get_json('role', role), 200)
                            
                    response = create_error('unexpected_error')
                    return (response, 500)
                else:
                    response = create_error('role_not_found')
                    return (response, 404)
            # Insert the new role, when it doesn't exist
            else:
                # Check for required arguments
                if name and not query.does_role_name_exist(name):
                    role = Role(None, name=name, 
                                description=description )
                    query.add_role(role)
                    response = get_json('role', role)
                    return (response, 200)
                elif name:
                    response = create_error('name_taken')
                    return (response, 400)
                else:
                    response = create_error('missing_argument')
                    return (response, 400)
                
        except Exception as e:
            print(e)
            response = create_error('unexpected_error', e)
            return (response, 500)
    
    elif request.method == 'DELETE':
        # role = query.get_role_by_id(role_id)
        try:
            if role_id:
                for x in role_id:
                    query.remove_role(role_id[0])
                return (json.dumps({}), 200)
            else:
                response = create_error('role_not_found')
                return (response, 404)
        except Exception as e:
            response = create_error('unexpected_error', e)
            return (response, 500)
            
            

@roles.route('/api/roles', methods = ['GET', 'DELETE'])
def roles_uri():
    args = request.get_json()
    
    if request.method == 'GET':
        try:
            roles = query.get_all_roles()
            return get_json('roles', roles)
            
        except Exception as e:
            print(e)
            response = create_error('unexpected_error', e)
            return (response, 500)
            
    elif request.method == 'DELETE':

        role_ids = args.get('ids')
        try:
            if role_ids:
                for x in role_ids:

                    query.remove_role(x)
                return (json.dumps({}), 200)
            else:
                response = create_error('role_not_found')
                return (response, 404)
        except Exception as e:
            response = create_error('unexpected_error', e)
            return (response, 500)

            
@roles.route('/api/roles/groups', methods = ['PUT'])
def add_groups_to_roles():
    
    args = request.get_json()
    
    if args is None:
        response = create_error('missing_argument')
        return (response, 404)
       
    updated_roles = []
    
    try:
        for role_id in args["role_ids"]:
            role = query.get_role_by_id(role_id)
            if role:
                for group_id in args["group_ids"]:
                    group = query.get_group_by_id(group_id)
                    if group:
                        role.groups.append(group)
                is_updated = query.update_role(role)
                if is_updated:
                    updated_roles.append(role_id)
                    
        return (json.dumps({"ok": True, "roles": updated_roles}), 200)
        
    except Exception as e:
        response = create_error('unexpected_error', e)
        return (response, 500)
        
 
        
        
        
         
            
            

        
            
            
            
            
    #  try:
    #         group_name = args.get('name')
    #         group_id = args.get('id')
            
            
    #         if group_name and group_id:
    #             group = Group(name = group_name, app_group_id= group_id)
    #             query.add_group(group)
    # except Exception as e:
    #         print(e)
    #         response = create_error('unexpected_error', e)
    #         return (response, 500)