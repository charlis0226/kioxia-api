import os
import kioxialib
import json

from dotenv import load_dotenv

from flask import Flask
from flask import jsonify
from flask import request,redirect,url_for

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from datetime import datetime
from datetime import timedelta
from datetime import timezone


API_SERVER_HOST = '127.0.0.1'
API_SERVER_PORT = 3000

app = Flask(__name__)
jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


# Login ---------------------------------------------------------------------------

@app.route("/api/riks/login/", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if kioxialib.checkValidation(username, password) != True:
        return jsonify({"msg": "Login Error"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

#-----------------------------------------------------------------------------------



# Getting All Risk Criteria --------------------------------------------------------

@app.route("/api/risk/behavior/criteria", methods=["GET"])
@jwt_required()
def criteria():
    return  json.dumps(kioxialib.getAllCriteria())

#-----------------------------------------------------------------------------------


# Getting User RiskValue -----------------------------------------------------------

@app.route("/api/risk/behavior/<username>", methods=['GET'])
@jwt_required()
def riskValue(username):
    return json.dumps(kioxialib.getUser(username),default=str)

#-----------------------------------------------------------------------------------


# Update Risk Criteria -------------------------------------------------------------
@app.route("/api/risk/behavior/criteria", methods=["PATCH"])
@jwt_required()
def updateCriteria():
    oldRiskValue = request.json.get("oldRiskValue", None)
    newRiskValue = request.json.get("newRiskValue", None)
    newLowrBound = request.json.get("newLowrBound", None)
    kioxialib.updateCriteria(oldRiskValue, newRiskValue, newLowrBound)
    return jsonify({"msg": "Update Success"}), 200

#-----------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host = API_SERVER_HOST, port = API_SERVER_PORT, debug = True)