from flask import Flask, render_template, request, redirect, jsonify
import json
import os
import jwt


# Function code


def authenticate(request):
    data = request.json or {}
    data.update(request.args)
    data.update(request.form)
    email = request.form.get('email')
    token = jwt.encode({'email': email}, secret(), algorithm='HS256')
    return jsonify({'jwt': token})

def authenticated(request):
    claims = None
    token = request.cookies.get('jwt')
    claims = jwt.decode(token, secret(), algorithms=['HS256'])
    return jsonify(claims)

def secret():
    return os.getenv('JWT_KEY', 'test')


# For running locally

app = Flask(__name__)


@app.route('/authenticate', methods = ['POST', 'GET'])
def r_authenticate():
   return authenticate(request)


@app.route('/authenticated', methods = ['POST', 'GET'])
def r_authenticated():
   return authenticated(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
