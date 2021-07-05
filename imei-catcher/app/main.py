from flask import Flask, render_template, send_from_directory, jsonify, redirect
from flask_basicauth import BasicAuth
from libs.helpers import *
from sys import path

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'poc'
app.config['BASIC_AUTH_PASSWORD'] = 'pocpocpoc'

basic_auth = BasicAuth(app)


@app.route("/", methods=["GET"])
@basic_auth.required
def main():
    return render_template("index.html")


@app.route("/api/check-format/<imei>", methods=["GET"])
@basic_auth.required
def api_check_imei(imei):
    if check_imei(imei):
        return jsonify({"result": True,
                        "message": "The IMEI is valid."})
    else:
        return jsonify({"result": False,
                        "message": "The IMEI is invalid."})


@app.route("/api/process/<imei>", methods=["GET"])
@basic_auth.required
def api_process_imei(imei):
    if check_imei(imei):
        if process_imei(imei):
            return jsonify({"result": True, "message": "Your stalked"})
        else:
            return jsonify({"result": False, "message": "Everything seems fine"})


ssl_cert = "{}/{}".format(path[0], 'cert.pem')
ssl_key = "{}/{}".format(path[0], 'key.pem')

app.run(host="0.0.0.0", port=8443, ssl_context=(ssl_cert, ssl_key), debug=False)
