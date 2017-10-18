from flask import Flask
from flask import abort
from flask import request
import requests
import uuid
import rocksdb
from subprocess import Popen, PIPE, STDOUT

app = Flask(__name__)


@app.route('/api/v1/scripts', methods=['POST'])
def save_file():
    db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
    if request.method == 'POST':
        key = uuid.uuid4().hex
        request.files['data'].save('/tmp/'+key+'.py')
        bkey = key.encode('utf-8')
        value = ('/tmp/'+key+'.py').encode('utf-8')
        db.put(bkey, value)
        return 'OK Script Id:'+key, 201


@app.route('/api/v1/scripts/<string:script_id>', methods=['GET'])
def get_script_id(script_id):
    db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
    rkey = script_id.encode('utf-8')
    rvalue = db.get(rkey).decode('utf-8')
    cmd = 'python3 '+rvalue
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    x = str(output)
    fop = len(x)
    finop = x[2:fop - 3]
    return str(finop), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
