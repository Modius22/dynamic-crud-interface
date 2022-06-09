import json

from flask import Flask
from flask_cors import CORS, cross_origin

import helpers.db as db

app = Flask(__name__)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/get_db_names")
@cross_origin()
def get_db_data():
    test = db.DB()
    data = test.get_table_names()
    return json.dumps(data)


@app.route("/<table>/get_table_structure")
@cross_origin()
def get_table_structure(table):
    test = db.DB()
    data = test.get_table_columns(table)
    return data


if __name__ == "__main__":
    app.run()
