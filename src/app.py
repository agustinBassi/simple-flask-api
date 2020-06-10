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

from flask import Flask, Response, abort, json, jsonify, request

#########[ Settings & Data ]###################################################

app = Flask(__name__)

# Put app configurations here, like endpoints, variables, and others.
app_config = {
    "PREFIX"    : "/",
    "APP_PORT"  : 5000,
    "key1"      : "value1",
    "key2"      : "value2"
}

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

#########[ Views (route resources) ]###########################################

@app.route(app_config.get("PREFIX") + '', methods=['GET'])
def get_app_config():
    # create response for all devices
    response = jsonify(app_config)
    # return the response with the status code
    return response, 200

@app.route(app_config.get("PREFIX") + '', methods=['PUT'])
def set_app_config():
    global app_config

    if not request.json:
        return json_response(
            {'error' : 'Impossible to parse request body'}, 422
            )

    app_config.update(request.json)
    response = app_config

    return json_response(response, 200)

#########[ Module main code ]##################################################

if __name__ == '__main__':
    app.run()

#########[ Enf of file ]#######################################################
