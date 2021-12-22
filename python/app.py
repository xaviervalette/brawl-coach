from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
	return "<h1>Je t'aime Biboune <3"

@app.route("/segolenelaplusbelle")
def segolene():
	return return_template('navbar.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)
