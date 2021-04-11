# Import Flask depencies
from flask import Flask

# Create an app
app = Flask(__name__)

@app.route('/')

def hello_world():

    return "Hello World"