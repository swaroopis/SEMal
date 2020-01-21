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


@app.route('/get_malonylation', methods=['GET', 'POST'])
def get_mal():
    data = request.get_json()
    pssm = data["pssm"].split('\n')
    spd3 = data["spd3"].split('\n')
    res = get_result(pssm, spd3, data['species'])
    return res


@app.route('/get_pssm', methods=['POST'])
def get_pssm():
    data = request.get_json()
    pssm = data["pssm"].split('\n')
    if len(pssm) <= 1:
        return 'bad format'
    with open('./pssm.seq', 'w') as f:
        f.write(data["pssm"])
    cmd = "./{} -query ./pssm.seq -db /Users/dipta007/my-world/gdrive/Thesis/MSCSE/PTM/code/EvolMal/Web_Server/BE/NR/nr -out pssm.out -num_iterations 3 -out_ascii_pssm pssm.pssm -inclusion_ethresh 0.001 -num_threads 4".format(psiblast)
    MyOut = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = MyOut.communicate()
    print(stdout)
    print(stderr)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)