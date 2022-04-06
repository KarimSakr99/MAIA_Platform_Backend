from flask import Flask
from funcs.routes import new_illness, new_user
from funcs.routes import skin, skin_cam
from funcs.routes import chest, chest_cam


app = Flask(__name__)


@app.route('/chest', methods=['POST', 'GET'])
def call_chest(): return chest()


@app.route('/chest/cam', methods=['POST', 'GET'])
def call_chest_cam(): return chest_cam()


@app.route('/skin', methods=['POST'])
def call_skin(): return skin()


@app.route('/skin/cam', methods=['POST'])
def call_skin_cam(): return skin_cam()


@app.route('/new_user', methods=['POST', 'GET'])
def call_new_user(): return new_user()


@app.route('/new_illness', methods=['POST', 'GET'])
def call_new_illness(): return new_illness()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
