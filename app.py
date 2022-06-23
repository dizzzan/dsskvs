from operator import contains
from flask import Flask, request

app = Flask(__name__)

kvs = {
    "a": "one",
    "b": "two",
    "c": "three"
}

@app.route("/")
def home():
    return "Dan's Key-Value Store"

# return all stored values
@app.route("/api/values")
def list():
    return kvs

# create new stored value
@app.route('/api/values', methods=['POST'])
def create(update=False):
    
    kv = request.get_json()

    if not 'key' in kv:
        return 'No key in request', 400
    if not 'value' in kv:
        return 'No value in request', 400
    
    k = kv['key']
    v = kv['value']

    if k in kvs:
        if not update:
            return 'Duplicate key', 409
        kvs[k] = v
    else:
        kvs.append({ k: v })

# get a stored value by key
@app.route('/api/values/<string:k>')
def get(k):
    return kvs[k]

# delete a stored value by key
@app.route('/api/values/<string:key>', methods=['DELETE'])
def delete(k):
    if contains(kvs.keys, k):
        del kvs[k]
    else:
        return 'Key not found', 404

# update an existing value
@app.route('/api/values', methods=['PUT'])
def update():
    create(True)