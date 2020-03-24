from flask import Flask, request, jsonify
import os
from pathlib import Path
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify("hundred thousand dollars for the cheapest ring on a * finger lil bitch")

@app.route('/new_shard', methods=['POST'])
def update_shard():
    r = request.form

    dpath = '/home/bins/' + r['user_id']
    os.chdir(dpath)

    print(os.getcwd())

    if Path(r['filename']).is_file():
        os.remove(r['filename'])
    
    with open(r['filename'], 'w') as file:
       file.write(r['encrypted_content'])

    return jsonify({'file': Path(r['filename']).is_file()})

@app.route('/retrieve', methods=['POST'])
def get_shard():
    r = request.form  # This will have a user's id in it (the container belongs to the organization.)
        
    shards = []  # List of individual file shards.

    bin = r['user_id']
    path = '/home/bins/'
    path += bin

    os.chdir(path)  # Enter the bin for a specific user's cases.

    for fname in os.listdir():  # Get all of the filenames of individual shards, collect them.
        shard_dump = get_shard_content(fname)  # This is the encrypted body of a single file.
        current_shard = (fname, shard_dump)  # This is a tuple containing the file name + content of a shard.
        shards.append(current_shard)  # Adds current shard to global list of shards.
    
    response = {"response": shards}
    return jsonify(response)


def get_shard_content(filename):
    shard_dump = ""
    with open(filename, 'r') as file:
        s = ""
        shard_dump = s.join(file.readlines())
        return shard_dump

if __name__ == "__main__":
    app.run()