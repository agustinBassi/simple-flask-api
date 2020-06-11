#!/usr/bin/python
###############################################################################
# Author: Agustin Bassi
# Date: June 2020
# Licence: MIT
# Brief: Project template to create super fast & simple REST API using Flask
# web framework. Due to the project nature of be the simplest Flask API, this
# code use a file for storage data. It doesn't implement data Models.
# For more complex project structure consider other projects looking at 
# https://github.com/agustinBassi or in Github.
###############################################################################

#########[ Imports ]########################################################### 

import os
import json

from flask import Flask, Response, abort, json, jsonify, request

#########[ Settings & Data ]###################################################

APP_CONFIG = {
    "HOST"          : "0.0.0.0",
    "PORT"          : 5000,
    "PREFIX"        : "/api/v1/",
    "DEBUG"         : True,
    "DB_FILE_PATH"  : "../db/db.json",
}
# Flask App object
app = Flask(__name__)
# Settings that will be modified by the user
module_data = {}

#########[ Utils ]#############################################################

def create_json_response(response, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(response),
        status=status_code
    )

def db_get_stored_data():
    # obtain the full db path
    full_db_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        APP_CONFIG["DB_FILE_PATH"]
    )
    # Read data from DB file
    stored_data = json.loads(open(full_db_file_path).read())
    # Print app data read
    print("Data readed from DB file: " + str(stored_data))
    # returns the data read from DB file as dict
    return stored_data

def db_save_data_to_file(data_to_store):
    # obtain the full db path
    full_db_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        APP_CONFIG["DB_FILE_PATH"]
    )
    # Save current data into DB file
    with open(full_db_file_path, 'w') as db_file:
        # save app data in json pretty mode
        json.dump(
            data_to_store, 
            db_file, 
            ensure_ascii=False, 
            indent=4
            )
    # Log the action to console
    print("Updated DB file with new app data")

#########[ Application Views (endpoints) ]#####################################

@app.route(APP_CONFIG["PREFIX"] + '', methods=['GET'])
def get_app_config():
    # create response for all devices
    response = APP_CONFIG
    # return the response with the status code
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/module_settings/', methods=['GET'])
def get_module_settings():
    # create response for all devices
    response = get_module_data()
    # return the response with the status code
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/module_settings/', methods=['PUT', 'POST'])
def set_module_settings():
    if not request.json:
        return create_json_response(
            {'error' : 'Impossible to parse request body'}, 
            422
            )
    # modify module data
    set_module_data(request.json)
    # obtain the current module data in a local variable
    local_module_data = get_module_data()
    # update DB file with new current module data
    db_save_data_to_file(local_module_data)
    # Send new current module data as response
    response = local_module_data
    return create_json_response(response, 200)

@app.route(APP_CONFIG["PREFIX"] + '/module_settings/', methods=['DELETE'])
def delete_module_settings():
    def __validate_request():
        # check the input data
        if not request.json.get("keys_to_remove") or type(request.json["keys_to_remove"]) is not list:
            return False
        # iterate over keys to check if they are strings
        for key in request.json["keys_to_remove"]:
            if type(key) is not str:
                return False
        # if reaches this point is a valid data
        return True
    # validate if there is data in request in JSON format
    if not request.json:
        return create_json_response(
            {'error' : 'Impossible to parse request body'}, 
            422
            )
    # check if request data is valid
    if not __validate_request():
        return create_json_response(
            {'error' : 'Bad request, it must be { "keys_to_remove" : ["key1", "key2"] }'}, 
            400
            )
    # modify module data
    delete_module_data(request.json["keys_to_remove"])
    # obtain the current module data in a local variable
    local_module_data = get_module_data()
    # update DB file with new current module data
    db_save_data_to_file(local_module_data)
    # Send new current module data as response
    response = local_module_data
    return create_json_response(response, 200)

#########[ Specific module code ]##############################################

"""
In this section the specific application code must be defined. In this simple 
example there are 3 function to get, set and delete module settings.

Here could be specific function such us open a connection to some server, get 
user inputs, and any other.

The funcions/methods created in this section must be called from functions in
views section. The existent functions can be used or new views can be created.
"""

def get_module_data():
    return module_data

def set_module_data(data_dict):
    global module_data
    module_data.update(data_dict)

def delete_module_data(keys_to_remove):
    global module_data
    for key in keys_to_remove:
        module_data.pop(key, None)

#########[ Module main code ]##################################################

def init_app():
    # obtain the module data saved previously in DB file
    local_module_data = db_get_stored_data()
    # update the module data with data read from DB file
    set_module_data(local_module_data)

if __name__ == '__main__':
    init_app()
    app.run(
        host=APP_CONFIG.get("HOST"), 
        port=APP_CONFIG.get("PORT"),
        debug=APP_CONFIG.get("DEBUG"),
        )

#########[ Enf of file ]#######################################################
