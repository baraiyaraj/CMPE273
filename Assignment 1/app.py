from flask import Flask
from flask import abort
from flask import request
import requests
import uuid
import rocksdb
#import subprocess

db = rocksdb.DB("Assignment1.db", rocksdb.Options(create_if_missing=True))
app = Flask(__name__)


@app.route('/api/v1/scripts', methods=['POST'])
def save_file():
    if request.method == 'POST':
       # f = request.files['data']
        key = uuid.uuid4().hex
        request.files['data'].save('/home/raj/Uploads/'+key+'.py')
        bkey = key.encode('utf-8')
        value = ('/home/raj/Uploads/'+key+'.py').encode('utf-8')
        db.put(bkey, value)
        return 'OK Script Id:'+key, 201


'''@app.route('/api/v1/scripts/<string:script_id>', methods=['GET'])
def get_script_id(script_id):
    rkey = script_id.encode('utf-8')
    rvalue = db.get(rkey)
    if rvalue != 0:
        foutput = subprocess.call(""+rvalue, shell=True)
        return foutput, 200
    else:
        return 'NOT FOUND', 404
'''

if __name__ == '__main__':
    app.run(debug=True)