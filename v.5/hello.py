from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Index page"

@app.route("/hello")
def hello():
    return "Hello, beautiful fucking world!"

if __name__ == "__main__":
    app.run(debug=True)