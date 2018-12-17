from flask import Flask, render_template, request, redirect, jsonify, make_response
import json
import os
import jwt


# Function code


def authenticate(request):
    data = request.json or {}
    data.update(request.args)
    data.update(request.form)
    email = data.get('email')
    token = jwt.encode({'email': email}, secret(), algorithm='HS256')
    return cors({'jwt': token.decode()})

def authenticated(request):
   claims = None
   data = request.json or request.args
   token = data.get("jwt")
   if token:
      claims = jwt.decode(token.encode(), secret(), algorithms=['HS256'])
   if claims:
      return cors(claims)
   else:
      return cors({})

def cors(data):
   if data:
      response = jsonify(data)
   else:
      response = make_response()
   response.headers['Access-Control-Allow-Origin'] = '*'
   response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
   response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
   return response

def secret():
    return os.getenv('JWT_KEY', 'test')


# For running locally

app = Flask(__name__)


@app.route('/authenticate', methods = ['POST', 'GET', 'OPTIONS'])
def r_authenticate():
   if request.method == 'OPTIONS':
      return cors({})
   else:
      return authenticate(request)


@app.route('/authenticated', methods = ['POST', 'GET', 'OPTIONS'])
def r_authenticated():
   if request.method == 'OPTIONS':
      return cors({})
   else:
      return authenticated(request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
