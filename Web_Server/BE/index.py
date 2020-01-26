from flask import Flask
from flask import jsonify
from flask import request
import platform
import subprocess
from utility import get_result
from flask_cors import CORS


psiblast = "psiblast_{}".format(platform.system())

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello():
    return "Hello World"


@app.route('/get_malonylation', methods=['GET', 'POST'])
def get_mal():
    data = request.get_json()
    pssm = data["pssm"].split('\n')
    spd3 = data["spd3"].split('\n')
    res = get_result(pssm, spd3, data['species'])
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
