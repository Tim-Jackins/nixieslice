import os
from flask import Flask, send_from_directory, request
from flask import jsonify, redirect
from time import sleep, time
import yaml
import pprint

app = Flask('Clock', static_folder='clock-app/build')
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True


pp = pprint.PrettyPrinter(indent=4)

configFile = 'sample.yml'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != '' and os.path.exists("clock-app/build/" + path):
        return send_from_directory('clock-app/build', path)
    else:
        return send_from_directory('clock-app/build', 'index.html')


@app.route('/api/config/', methods=['GET','POST'])
def config():
    global configFile
    if request.method == 'GET':
        configYaml = open(configFile, "r")
        config = yaml.load(configYaml)
        return jsonify(config)
    else:
        data = request.form
        configYaml = open(configFile, "r")
        config = yaml.load(configYaml)

        for i in range(10):
            config['Lights'][ data['num'] ][i]['brightness'] = data[f'bright-slice-{i}']
            config['Lights'][ data['num'] ][i]['color'] = data[f'color-slice-{i}']

        with open(configFile, 'w') as outfile:
            yaml.dump(config, outfile, default_flow_style=False)

        return redirect('/')


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000)
