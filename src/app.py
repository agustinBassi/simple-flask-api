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

DB_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "../db/db.json"
)
# Flask App object
app = Flask(__name__)
# Application config dict
app_data = {}

#########[ Utils ]#############################################################

def json_response(response, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(response),
        status=status_code
    )

def load_app_data_from_db_file():
    global app_data
    # Read data from DB file
    app_data = json.loads(open(DB_FILE_PATH).read())
    # Print app data read
    print("Data readed from DB file: " + str(app_data))

def save_current_app_data_to_db_file():
    # Save current data into DB file
    with open(DB_FILE_PATH, 'w') as db_file:
        # save app data in json pretty mode
        json.dump(
            app_data, 
            db_file, 
            ensure_ascii=False, 
            indent=4
            )
    # Log the action to console
    print("Updated DB file with new app data")

#########[ Views (route resources) ]###########################################

@app.route('/', methods=['GET'])
def get_app_config():
    # create response for all devices
    response = app_data
    # return the response with the status code
    return json_response(response, 200)

@app.route('/', methods=['PUT'])
def set_app_config():
    global app_data

    if not request.json:
        return json_response(
            {'error' : 'Impossible to parse request body'}, 
            422
            )

    app_data.update(request.json)
    save_current_app_data_to_db_file()
    response = app_data

    return json_response(response, 200)

#########[ Module main code ]##################################################

def init_app_data():
    load_app_data_from_db_file()

if __name__ == '__main__':
    init_app_data()
    app.run(
        host=app_data.get("APP_HOST"), 
        port=app_data.get("APP_PORT"),
        debug=app_data.get("APP_DEBUG"),
        )

#########[ Enf of file ]#######################################################
