from flask import Flask, request, Response
import jwt
from datetime import timedelta, datetime
app = Flask(__name__)

users = [
    {'username': 'uli', 'password': 'mypassword'},
    {'username': 'eve', 'password': 'mypassword2'},
    {'username': 'caio', 'password': 'mypassword3'},
]

@app.route("/authenticate", methods = ['POST'])
def authenticate():
    try:
        body = request.get_json()
        username = body['username']
        password = body['password']
        # Check if the user is authorized:
        for user in users:
            if user['username'] == username and user['password'] == password:
                # Authentication succeeded
                claims = {
                    "iss": "cct",
                    "sub": username,
                    "aud": "users",
                    "exp": (datetime.now() + timedelta(minutes = 5)).timestamp(),
                    "iat": datetime.now().timestamp(),
                    "role": "user"
                }
                return {'token': jwt.encode(claims, "this-is-a-secret", algorithm="HS256")}                
    except:
        return Response('Unauthorized', 401)
    return Response('Unauthorized', 401)

if __name__ == '__main__':
    app.run()