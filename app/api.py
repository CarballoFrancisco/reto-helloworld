import http.client
from flask import Flask
from app import util
from app.calc import Calculator

CALCULATOR = Calculator()
api_application = Flask(__name__)
HEADERS = {"Content-Type": "text/plain", "Access-Control-Allow-Origin": "*"}


@api_application.route("/")
def hello():
    return "Hello from The Calculator!\n"


@api_application.route("/calc/add/<op_1>/<op_2>", methods=["GET"])
def add(op_1, op_2):
    try:
        num_1 = util.convert_to_number(op_1)
        num_2 = util.convert_to_number(op_2)
        result = CALCULATOR.add(num_1, num_2)
        return ("{}".format(result), http.client.OK, HEADERS)
    except TypeError as e:
        error_message = str(e)
        return (error_message, http.client.BAD_REQUEST, HEADERS)


@api_application.route("/calc/subtract/<op_1>/<op_2>", methods=["GET"])
def subtract(op_1, op_2):
    try:
        num_1 = util.convert_to_number(op_1)
        num_2 = util.convert_to_number(op_2)
        result = CALCULATOR.subtract(num_1, num_2)
        return ("{}".format(result), http.client.OK, HEADERS)
    except TypeError as e:
        error_message = str(e)
        return (error_message, http.client.BAD_REQUEST, HEADERS)

