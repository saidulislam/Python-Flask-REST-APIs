from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return("Hello World!")


# it will run on default port 5000
app.run(debug=True)