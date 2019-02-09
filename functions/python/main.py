from flask import Flask, render_template, request, redirect, jsonify, make_response
import json
import os
import jwt
import bcrypt
import hashlib
import base64
from google.cloud import datastore


# Function code

def register(request):
   data = request.json or {'name': 'David Carboni', 'email': 'david.carboni@notbinary.co.uk'}
   data.update(request.args)
   data.update(request.form)
   email = data.get('email')
   name = data.get('name')
   password = data.get('password')

   if email:
      client = datastore.Client(project_id())

      # Check for an existing user
      if read(email, client):
         return "This email is already registered.", 400

      # Create a record for this user
      user = create(email, name, password, client)
      print(f'Registered: {user}')
      result = read(email, client)
      print(f're-read: {result}')
      token = jwt.encode({'name': result.name, 'email': result.email}, secret(), algorithm='HS256')
      print('jwt: {token.decode()}')
      return cors({'jwt': token.decode()})
   else:
      return "Please provide a value for 'email' (and optionally 'name' and 'password')", 400

def authenticate(request):
   data = request.json or {}
   data.update(request.args)
   data.update(request.form)
   email = data.get('email')
   password = data.get('password')
   if email and password:
      client = datastore.Client(project_id())
      user = read(email, client)
      if user and check_password(user.get('password')):
         token = jwt.encode({'email': email}, secret(), algorithm='HS256')
         return cors({'jwt': token.decode()})
   return cors({})

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

def create(email, name, password, client):

   if email:

      client = datastore.Client(project_id())

      if read(email, client):
         return False

      key = client.key('User')
      entity = datastore.Entity(key=key)
      entity.update({
         'email': email.lower().strip(),
         'name': name,
         'password': hash_password(password),
      })
      client.put(entity)
      print(f'Created: {entity}')
      return True

   return False

def read(email, client):
      q = client.query(Kind='User')
      q.add_filter('email', '=', email.lower().strip())
      q_iterator = q.fetch(limit=1)
      page = next(q_iterator.pages)
      users = list(page)
      if len(users) > 0:
         print(f'Read: {users[0]}')
         return users[0]
      else:
         return None

def hash_password(password):
   # See https://github.com/pyca/bcrypt/
   return bcrypt.hashpw(
      base64.b64encode(hashlib.sha256(password).digest()),
      bcrypt.gensalt()
   )

def check_password(password):
   # See https://github.com/pyca/bcrypt/
   return bcrypt.checkpw(
      base64.b64encode(hashlib.sha256(password).digest())
   )

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

def project_id():
   """Gets the GCP project ID
   NB there's nothing the requester can do if this hasn't been set, so
   if it's missing we abort with a 500 and log what's not been configured.
   """
   project_id = os.getenv('PROJECT_ID')
   if not project_id:
      raise Exception("Pleaste set a PROJECT_ID environment variable.")


# For running locally

app = Flask(__name__)


@app.route('/register', methods = ['POST', 'GET', 'OPTIONS'])
def r_register():
   if request.method == 'OPTIONS':
      return cors({})
   else:
      return register(request)


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
