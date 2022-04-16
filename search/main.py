from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
import io
import jwt
import minio
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open('index.html') as f:
        return f.read()
   

@app.route("/search")
def search():
    #try:
     #   token = request.header.get('Authorization').split(' ')[1]
      #  jwt.decode(token, "test", algorithms=["HS256"], audience='users')
    #except:
     #   return "unauthorized", 401
    searchTerm = request.args.get('term')
    matchedSongs = []
    client = minio.Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False)
    
    objects = client.list_objects(bucket_name="cctmsc")
    for object in objects:
        if object.object_name.endswith('.json'):
            fullObject = client.get_object("cctmsc", object.object_name)
            file_content = ''
            for d in fullObject.stream():
                file_content += d.decode('utf-8')

            dict_object = json.loads(file_content)
            dict_object['mp3'] = object.object_name.split('.')[0] + '.mp3'
            if searchTerm in dict_object['author'] or searchTerm in dict_object['title']:
                matchedSongs.append(dict_object)
    return jsonify(matchedSongs)

@app.route("/get")
def get():
    song = request.args.get('song')
    client = minio.Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False)
    full_song = client.get_object("cctmsc", song)
    mp3bytes = bytearray()
    for data in full_song.stream():
        mp3bytes += data
    response = make_response(mp3bytes)
    response.headers.set('Content-Type', 'audio/mpeg')
    return response

if __name__ == '__main__':
        app.run()