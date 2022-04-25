from flask import Flask
from funcs.routes import new_illness, new_user
from funcs.routes import skin, skin_cam
from funcs.routes import chest, chest_cam
from funcs.routes import hip, hip_animation

app = Flask(__name__)


@app.get('/')
def root(): return 'MAIA Running'


@app.post('/chest')
def call_chest(): return chest()


@app.get('/chest/cam')
def call_chest_cam(): return chest_cam()


@app.post('/skin')
def call_skin(): return skin()


@app.get('/skin/cam')
def call_skin_cam(): return skin_cam()


@app.post('/hip')
def call_hip(): return hip()


@app.get('/hip/gif')
def call_hip_animation(): return hip_animation()


@app.post('/new_user')
def call_new_user(): return new_user()


@app.post('/new_illness')
def call_new_illness(): return new_illness()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
