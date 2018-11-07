from flask import Flask, render_template, request
from mage import make_map
from PIL import Image

app = Flask(__name__)


@app.route("/")
@app.route("/ego.html")
def homepage():
    return render_template('ego.html', title='ego')


@app.route("/mage")
@app.route("/mage.html")
def mage():
    return render_template('mage.html', title='mage')


@app.route("/mage_run_template", methods=['POST'])
def mage_run_template():
    size = request.form.get("size")
    background = Image.new('RGB', (int(size), int(size)), 'black')
    return make_map(size, background)

@app.route("/gwm")
@app.route("/gwm.html")
def gwm():
    return render_template('gwm.html', title='gwm')


if __name__ == '__main__':
    app.run(debug=True)